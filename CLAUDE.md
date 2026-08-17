# Project summary

We are building a Factorio-themed harness in public, with published "engineer notes" every 1-3 days. 

# Why I am doing this

After almost 1000 hours building with Claude I've realized that even though I thought I wasn't from a technical background, that my similar number of hours in Factorio over the last decade actually significantly impacts the way I build. 

So I'm building this as a fun, public facing demo. The public facing part is really important!

## Business motives

I am also trying to fix the issue of my ai operator capabilities being completely illegible to other people.
-  to CTOs because I'm from a marketing background and my CV doesn't match what they're looking for.
-  to my target ICP: mid-sized marketing agency leadership who I'm trying to provide b2b ai engineering services to.
-  to get noticed by the builder community due to this being a fun and interesting build.
-  to potentially team up with creators of Factorio (I'm in Czechia like them) to partner to offer a "Learn AI via Factorio" course.

## Operator improvement goals

- The theme of this project will force me to get better at some of the more deterministic toolkit that might come a bit more naturally from other from a more tech-background than mine. For example:
  
	- System architecture / design
	- Traceable routing
	- Loops
	- YAML frontend
	- pre-tool hooks
		- especially around enforcing fence for creative constraints -- no cheating!
	- granular subagent settings
	- Clobber prevention with multiple parallel, working directory sessions on the same local machine / repo
		- Not using separate worktrees though
			- a.) this is about artifakt logistics, everyone needs to see the same state
			- b.) as a creative constraint to be forced to learn to work around
	- This is a non-exhaustive list.

### Assistant-led learning opportunities

- If you see me trying to avoid the improvement goals by using prose-based instructions I'm used to, call it out and turn it into a learning opportunity. 
- We will build a Lab soon, don't worry!

### Assistant behaviors to avoid

- Because this build is about exact, granular settings. Do not guess or pattern match for things like front header variables, file output locations, or naming conventions. Enforce explicit design by the operator.
- Do not crawl the file tree to figure out context. Always ask the operator when unsure where to look to find something.
- This is a Factorio THEMED build, but don't go overboard. I'm still trying to demonstrate my ai engineering capabilities, so let's have fun, but not get lost in role play. This is a fun -- yet professional -- project.

# Architecture overview

The parent folder Factor-AI, which is a public repo and has Claude initiated, will hold many subfolders. Many of those child subfolders will be claude working directories as well.

## Architecture capabilities and limitations research

- Lazy load -- only when needed -- "C:\Users\alder\Desktop\Factor-AI (staging)\granular-control.md"

# Building in public

As stated above, this is of top concern. Until we build something more sophisticated, we will have full transcripts to fall back on. 

## How to preserve narrative in git commits

please commit frequently and freely, using commit messaging that is detailed and narrative oriented. We will need to post hoc cut the building into 4-6 minute updates, so back sure your commits enable this.

### Publishing format

Currently out of scope. Just preserve everything needed to make that possible in the future.

