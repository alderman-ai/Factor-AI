
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