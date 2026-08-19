
## The build -- officially starting at 11:32

- `_THE SHIP/`
- The Guy/ (cwd)
	- ADRENALINE
- Power Station (cwd)
	- POWER
- Electric Pole-001/
- Crate-001-v/
- Inserter-002
- Belt-003-ii/
- Mining Station (cwd)
	- Generator-001/
		- POWER
	- Belt-002/
	- Ore-Patch-001-v/
			- ORE
		- Belt-001-ii/
		- Inserter-001

## DoD

The guy must use Human Actions to Move 5 pieces of Ore into THE SHIP

Which means 3 parallel sessions. All resources generating on loops. ALL ON THE SAME BRANCH (main) because everyone needs to see the whole state of the filetree - this is file logistics. My stomach hurts already.


# Notes

## 1143

who controls the inserters? WHO CONTROLS THE INSERTERS. And belts.

Do I need another cwd managing it, or can I set up some 'new file' watcher and have it actually be automated.

oh god, how do i enforce power. if power needs enforcement, then the transport can't be automated (like actually automated not what-the-hell-am-i-even-doing-here "automated")

ughhh do i just start with ore...

ON YOUR FIRST DEMO!? Figure it out!

Look, just add a starter base in charge of automated transportation. But then the file tree gets messy because

Oh I never explained ANY of the ontology of transportation. Sorry! No time now 

## 1152

Is it stupid that i'm building all this by hand? like ... the infrastructure? Is that creative constraint or dumb... feels dumb. But first demo will continue. 

OK clarity (ish)

Power transport mirrors automated transport

### Power

Power is generated in Station on a loop. The power station also directs the movement of power. But it can't just git move power anywhere. An electric pole is the enablement of horizontal movement of power (ehhhh kind of ... so power is a child of power station ... but it feels dumb to have a new component pull it up ... for now at least). Ok so electric pole for horizontal movement, to a generator which can hold it. The first generator must be in same dir as powerstation. Generators can transfer power up or down the tree by one step. Each Power must have it's routing tracked the whole time.

Routing example
Power is created at time by place
Power moved from place a to b
via pole y
from gen a to gen b
consumed by x automated action and sent to consumed... we need a consumed/

and maybe power isn't consumed... I think we landed on that. It sits in a generator. If the generator has enough power to run all machines then the machines in that dir will function. If not, they wont. **It's binary**

So game play will be ... power station IS NOT generating power on loop. It has a fixed amount. It's just moving the power around. And there's not enough power for everything. So first it powers the mine to generate enough power to get it to the Demo/Belt-003. Then then power needs to be moved via the station to the top levle generator for the transport to bring it to Crate. (fun! ?)

### Transport -- 12:06

Belt is to Substation as Inserter is to Electric Pole
Belts move artifacts up and down a tree, inserters horizontal. Both tag routing

## Routing tags

I think it's not scalable to have them in YAML header. Maybe a log on each artifact that lists routing item and time? Maybe only the Poles and Inserters leave routing info? 

Attempt: Power Station to Substation-001 HHmm (Success | Failed)

(ughhh how to I build tables in md)

Theres so many primitives I need to build for all this to work the first time

## 12:15

Ok, for now the execution of movement will just be root Faktor-AI/ not building a new parent folder for all this. But Now that's actually a problem because I don't want to be cwd's into a parent and child simultaneously?? Do I? lets see if it break anything YOLO

ok that's a simple skill to build (the god laugh)

hard part is, how to know if the powered automation is alive or not

**THIS IS WHY YOU START WITH HAND MINING IN THE GAME WOULDN"T THAT BE A BETTER DEMO 1???**

Ok, the guy processes Adrenaline templated intake to do his actions. ... maybe power IS consumed? Huge fork ... :( Because it's not consumed via movable, it's executable file vs .... ???

## 12:21

Ok, let's work backwards. dod is human moves ore from crate to ship. Let's write that first.

Commit (sub demo 1 begins)

**1226** (omg im literally screenshotting factorio images to turn into icos for the folders FOCUS!)

noooww looking up an obsidan plugin for note duplication naming configuration 🙃

I have a meeting at 13 ... PLEEEASE don't forget to go to your meeting


ooooh i can record audio notes via obsidian and then think aloud and not type so much cool! (next time)

hmm didn't find name duplicater ... but Context Titles look cool for other projects FOCUS! **1237**


**12:50** just realized i didn't have gitkeeps in any folders so half the contents were missing AND realizing we're going to have to solve the parent-child problem, which is actully a thing. I guess just designate fence to include sister dirs in each cwd claude.md?

MEETING! 12:59 (paused)

## 15:50 Unpaused

I'll be honest, this is one of those projects where a three hour break really makes you not want to jump back in lol. Ok, let's see how far I can get.

First thought is, I need to set rules for myself about what needs to be built by hand. **Automated or by hand paper over different problems**. Automated, I don't need to worry about thinking about the best way to do the more tedious stuff. By hand I don't have to worry about info/context management. 

... I should probably do this stuff by hand, the tedious stuff is the whole point. : /

I'm also learning how obnoxious it is to give boundaries on your llms and expect them to know when they shouldn't apply. Prob an important less there too. Probably all skill building and world building will happen at the root cwd, if I have another agent tell me the document i linked them is outside their fence, i'm going to just stop this project lol


1611 -- oh no, they're going to try and make me learn python...




## 1629

Ok, I'm going to have an intake form for python verification codes. I'm not learning a scripting language but I will make the verification deterministic, not prose.

List of verbs in schema, verification script in Instrument Panel. will clean everything at some point.

## Fully path to DoD, articulated

- PowerStation starts generating power - no idea how -- good start
- PowerStation needs to route enough power to mining station to have it's transportation elements work
- Power is binary, either the directory is powered or not. Lets say for now each belt and inserter cost 1 power. Let's restrict it so you need to move power to mine, but there isn't enough left over to get inserter-001 to work, so you needed to move power back and forth a couple times. 
- So well have 3 total power.
- Once powered (how to check for or indicate this?),
- Then the Ore Patch will generate 1 ore every x seconds. A powered inserter will move an ore from the patch to the belt every x seconds. the belt will move to the belt one step up in the filetree every x seconds.
- Then the machine will freeze up. Because Belt-002-ii and Belt-001-ii will each have 2x ORE, and the ii means they can only hold 2 things. And inserter-001 is unpowered so it can't clear the belt. So powerstation moves power to higher level substation, then the belt is cleared, then power back to mines, the belt is refilled, then power back to top to get all ore to crate.
- Then it's just a human action thing. Spending adrenaline to move ore from crate to ship 5x times.
- But, for the Ship to accept the ore, the ORE's routing must be pattern matched.

Routing for ore happens at these stages:
- Generated at ore patch
- Moved from ore patch to Belt-002-ii **via** inserter-002
- Moved from Belt-002-ii to Belt-001-ii 
- Moved from Belt-001-ii to Crate-001-v **via** inserter-001
- Moved from Crate-001 to Demo Ship **with** Human Action **by** @The Guy

So, log or frontheader... has to be frontheader because minimal prose is literally the forcing function for all of this

Ok, I think I want the full pathing to be translated into a string to easily check if the exact pathing matches expectations

Ok here's the above mentioned frontheader:

Category: Resource
Inert: "True"
Type: Ore
Kind:
Session UUID:
Originates at: Ore Patch-001-iii
Origin Time: 2026-08-19T17:04:00
R-001-To: Belt-002-ii
R-001-Via: Inserter-002
R-002-To: Belt-001-ii
R-003-To: Crate-001-v
R-003-Via: Inserter-001
R-004-To: Demo Ship
R-004-With: Human Action
R-004-By: "@The Guy"
R-end: 2026-08-19T18:19:00

So, if I turn that into a verification string... by hand once, then build a script ...

o-op1-r1tb2vi2-r2tb1-r3tc1vi1-r4tSHIPwHAbGUY

this is ai psychosis i'm going home

(need for tomorrow schema of routing shorthand)

also, fill need times for all routes... but checksums will contain only start and end (in case theres a timelimit before decay ...... AI PSYCHOSIS)

o-202608191704-op1-r1tb2vi2-r2tb1-r3tc1vi1-r4tSHIPwHAbGUY-202608191819-e