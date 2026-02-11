Discuss: Arch, Dream, Smith: Upgrade day_dream system:

We will intergrate the "Decomposition Rules for Engineering Atomic Modules" (short form: DREAM)

1. First of all, fix the current blueprint planning system, the current system:
1a. The estimation of task is too long, some "1 week" can be done by AI agent in half an hour. The standard should be base on AI agents, not human, unless that task is fundamantal can only be done by human.
1b. The blueprints written by Dream / even the implementations by Arch, are too focus on "backward compatibility", for a system on a on-going development, with no old data, or those old data should be updated, should not think about "backward compatibility" at all! AI agents too focus on that I think is because they are too afrad to break anything (those no clue vibe coding user will be unhappy). But this ADHD framework is not, should not, and will not be a vibe code framework. And should prioritize clean, correct code, not minimize edited lines, nor millons of fallback to old (often wrong) code. 
1ba. For the case that should consider backward compatibility, do not do that side by side (try (new correct code) catch (old wrong code)), instead, break out a file for old path / new path, with clean and clear seperated folder structure, that dev can just delete the old path once the migration is done. 
1c. Current blueprints set always have "walking skeleton", some short tasks should not be break down to "walking skeleton", forcing "walking skeleton" will add complexity on those simple tasks, make them even harder. The original objective for walking skeleton is to pull some testing closer to p0, e.g. you don't write the full web frontend before writing the backend. But we should not make "walking skeleton" for those task by their nature can be tested at any phase. (should still break to phase though if the task is big, just no walking skeleton.)

2. update to use Decomposition Rules for Engineering Atomic Modules:
2a. The current blueprints set template is linear, and tedious on updating single point, e.g. a point can also appear on index and excutive summary and many other place.
2b. DREAM_v3.md is a doc for the new DREAM system, but the Recommended Folder Layout is not for ADHD framework, the folder structure is chaotic (some "node" are folder but some are files.), we should figure out a way to make it better, uniformed. And the term "node" is confusing too.
2c. the best part of this DREAM system is modular and Context Isolation, Sibling Firewall, creating multi-subagents to create and update specific branch, fixing the problem I mentioned above.
2d. I think it lag a very clear instruction for creating and updating the blueprints, I think we should create a skill for that?

After the above discussion, create a blueprints set for the whole dream system update (with above 2 parts), the blueprints set should be using current existing blueprint templates, not the new ones in DREAM_v3.md, do not transfer to new system before we have the new system ready.