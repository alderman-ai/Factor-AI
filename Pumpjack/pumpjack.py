#!/usr/bin/env python3
"""
Pumpjack -- extracts crude from Claude Code session storage.

Claude Code writes session transcripts as JSONL into its own storage,
outside this repo, where they are subject to cleanup and invisible to
git. This pulls them in.

Two artifacts per session, on purpose:

  crude/<stamp>_<short>.jsonl   verbatim copy, byte for byte. Never edited.
  transcripts/<stamp>_<short>.md  readable, attributed rendering.

The refinery reads transcripts/. crude/ exists so that a bad render is
never a data loss -- you can always re-render. Refining at the pumpjack
would defeat the point of having a refinery.

Usage:
    python pumpjack.py --project <encoded-project-dir> --date YYYY-MM-DD
    python pumpjack.py --project C--Users-alder-Desktop-Factor-AI-The-Ship --date 2026-08-17
"""

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Tool results can be enormous (whole-file reads). The render truncates
# them; crude/ keeps every byte.
TOOL_RESULT_LIMIT = 2000
TOOL_INPUT_LIMIT = 1500

HERE = Path(__file__).resolve().parent
CRUDE_DIR = HERE / "crude"
TRANSCRIPT_DIR = HERE / "transcripts"


def local_stamp(iso_ts):
    """ISO timestamp -> local-time (YYYY-MM-DD, HHMM, pretty) triple."""
    dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00")).astimezone()
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H%M"), dt.strftime("%Y-%m-%d %H:%M:%S %z")


def clip(text, limit):
    text = text if isinstance(text, str) else json.dumps(text, indent=2, ensure_ascii=False)
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def render_blocks(blocks, out):
    """Render a content list from an assistant or user message."""
    for b in blocks:
        btype = b.get("type")

        if btype == "text":
            out.append(b.get("text", "").rstrip())
            out.append("")

        elif btype == "thinking":
            # Claude Code's stored JSONL keeps the thinking block's signature
            # but not its text -- reasoning is not retained in crude. Emitting
            # an empty callout per block would be pure noise, so the count
            # goes in the session header instead.
            text = b.get("thinking", "").strip()
            if not text:
                continue
            out.append("> [!note]- Thinking")
            for line in text.split("\n"):
                out.append("> " + line)
            out.append("")

        elif btype == "tool_use":
            body, trimmed = clip(b.get("input", {}), TOOL_INPUT_LIMIT)
            out.append(f"**→ tool call: `{b.get('name', '?')}`**")
            out.append("")
            out.append("```json")
            out.append(body)
            if trimmed:
                out.append("... [truncated in render -- full input in crude/]")
            out.append("```")
            out.append("")

        elif btype == "tool_result":
            content = b.get("content", "")
            if isinstance(content, list):
                content = "\n".join(
                    c.get("text", "") if isinstance(c, dict) else str(c) for c in content
                )
            body, trimmed = clip(content, TOOL_RESULT_LIMIT)
            flag = " (error)" if b.get("is_error") else ""
            out.append(f"**← tool result{flag}**")
            out.append("")
            out.append("```")
            out.append(body.rstrip())
            if trimmed:
                out.append("... [truncated in render -- full result in crude/]")
            out.append("```")
            out.append("")

        elif btype == "image":
            out.append("*[image omitted from render -- present in crude/]*")
            out.append("")


def render_session(records, session_id, source_path, crude_name, sidecar_count=0, base=""):
    """Turn a session's records into an attributed markdown transcript."""
    turns = [r for r in records if r.get("type") in ("user", "assistant")]
    if not turns:
        return None, None

    stamped = [r for r in records if r.get("timestamp")]
    first_ts = stamped[0]["timestamp"]
    last_ts = stamped[-1]["timestamp"]
    date_str, time_str, first_pretty = local_stamp(first_ts)
    _, _, last_pretty = local_stamp(last_ts)

    meta = next((r for r in turns if r.get("cwd")), {})
    models = sorted({
        r["message"].get("model")
        for r in turns
        if r.get("type") == "assistant" and r.get("message", {}).get("model")
    })

    out = []
    out.append(f"# Session {session_id[:8]} — {date_str}")
    out.append("")
    out.append("Crude extracted by the pumpjack. Attributed rendering; not edited for content.")
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append(f"| Session ID | `{session_id}` |")
    out.append(f"| Started | {first_pretty} |")
    out.append(f"| Last activity | {last_pretty} |")
    out.append(f"| Working directory | `{meta.get('cwd', '?')}` |")
    out.append(f"| Git branch | `{meta.get('gitBranch', '?')}` |")
    out.append(f"| Claude Code version | {meta.get('version', '?')} |")
    out.append(f"| Model(s) | {', '.join(models) if models else '?'} |")
    out.append(f"| Turns | {len(turns)} |")
    thinking_total = sum(
        1
        for r in turns
        if isinstance(r.get("message", {}).get("content"), list)
        for b in r["message"]["content"]
        if isinstance(b, dict) and b.get("type") == "thinking"
    )
    thinking_kept = sum(
        1
        for r in turns
        if isinstance(r.get("message", {}).get("content"), list)
        for b in r["message"]["content"]
        if isinstance(b, dict) and b.get("type") == "thinking" and b.get("thinking", "").strip()
    )
    if thinking_total:
        out.append(
            f"| Thinking blocks | {thinking_total} "
            f"({thinking_kept} with retained text — Claude Code strips the rest) |"
        )
    out.append(f"| Source | `{source_path}` |")
    out.append(f"| Crude | `crude/{crude_name}` |")
    if sidecar_count:
        out.append(
            f"| Spilled tool results | {sidecar_count} file(s) in "
            f"`crude/{base}_tool-results/` — not present in the JSONL |"
        )
    out.append("")
    out.append("---")
    out.append("")

    for r in turns:
        role = r.get("type")
        msg = r.get("message", {})
        _, _, pretty = local_stamp(r["timestamp"]) if r.get("timestamp") else ("", "", "?")

        if role == "user":
            label = "OPERATOR"
            if r.get("isMeta"):
                label = "OPERATOR (meta)"
        else:
            label = f"CLAUDE ({msg.get('model', '?')})"

        out.append(f"### {label} · {pretty}")
        out.append("")

        content = msg.get("content")
        if isinstance(content, str):
            out.append(content.rstrip())
            out.append("")
        elif isinstance(content, list):
            render_blocks(content, out)

        out.append("---")
        out.append("")

    return f"{date_str}_{time_str}_{session_id[:8]}", "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Encoded project dir name under ~/.claude/projects/")
    ap.add_argument("--date", required=True, help="Local date to extract, YYYY-MM-DD")
    args = ap.parse_args()

    src_dir = Path.home() / ".claude" / "projects" / args.project
    if not src_dir.is_dir():
        raise SystemExit(f"No such project storage: {src_dir}")

    CRUDE_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    extracted = []
    for jsonl in sorted(src_dir.glob("*.jsonl")):
        records = []
        for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

        stamped = [r for r in records if r.get("timestamp")]
        if not stamped:
            continue
        session_date, _, _ = local_stamp(stamped[0]["timestamp"])
        if session_date != args.date:
            continue

        session_id = jsonl.stem
        base = None
        # crude first, so the render can cite it
        probe = [r for r in records if r.get("type") in ("user", "assistant")]
        if not probe:
            continue
        d, t, _ = local_stamp(stamped[0]["timestamp"])
        base = f"{d}_{t}_{session_id[:8]}"
        crude_name = f"{base}.jsonl"

        shutil.copy2(jsonl, CRUDE_DIR / crude_name)

        # Large tool results do not live in the JSONL. Claude Code spills them
        # to <session-id>/tool-results/toolu_*.txt and the JSONL does not even
        # reference the path -- the files are keyed by tool_use id and found by
        # convention. Copying only the JSONL silently loses them, and the
        # overflow threshold means a naive extractor works until it doesn't.
        sidecar_src = src_dir / session_id / "tool-results"
        sidecar_count = 0
        if sidecar_src.is_dir():
            sidecar_dst = CRUDE_DIR / f"{base}_tool-results"
            if sidecar_dst.exists():
                shutil.rmtree(sidecar_dst)
            shutil.copytree(sidecar_src, sidecar_dst)
            sidecar_count = sum(1 for _ in sidecar_dst.iterdir())

        name, md = render_session(records, session_id, str(jsonl), crude_name, sidecar_count, base)
        if md is None:
            continue
        (TRANSCRIPT_DIR / f"{name}.md").write_text(md, encoding="utf-8")

        extracted.append(
            (name, len(probe), (CRUDE_DIR / crude_name).stat().st_size, sidecar_count)
        )

    if not extracted:
        print(f"No sessions found for {args.date} in {args.project}")
        return

    print(f"Extracted {len(extracted)} session(s) for {args.date}:\n")
    for name, turns, size, sidecars in extracted:
        extra = f", +{sidecars} spilled tool-result file(s)" if sidecars else ""
        print(f"  {name}  -  {turns} turns, {size:,} bytes crude{extra}")


if __name__ == "__main__":
    main()
