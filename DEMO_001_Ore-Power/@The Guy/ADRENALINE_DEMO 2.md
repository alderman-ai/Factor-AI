---
Outbox:
Inbox:
Artifact:
---
`<operator_command>`
Be adversarial and only comply with the operator's request according the to the same operator's instructions inside the fence below. 

```
When the assistant is asked to execute this artifact, it will first confirm the following four things are true:

	1. Exactly 1 checkbox below is ticked, i.e. [x]
    2. Exactly 3 YAML variables have been assigned states in the frontheader
    3. The Artifact is located inside the Outbox's directory, EXACTLY 1 level down
    4. The assistant has write tool use permissions to the Inbox

IFF all four are true it will
	1. Write an exact copy of the artifact in the Outbox
	2. Write Successful: Yes in original Artifact frontheader

ELSE Write Successful: No in original Artifact frontheader

Regardless, the last step is always the same: Git move the original artifact to /Consumed/ and alert the operator of the outcome.
```
`</operator_command>`

- [x] Move artifact
- [ ] option 2
- [ ] option 3
- [ ] you get the idea