Manual Reasoning Notes:
This is a slowed-down example of how the logic system works. It's neat to be able to look under the hood and figure out how it all works. I found it good practice to always ask both if a tile is safe and unsafe, as the double-negative is a weakness of the logic. As I explain in the Reflection, the agent can struggle when it can't prove something.


Testing Notes:
Runing the agent with the example layout resulted in a success. It completed its task in 23 steps and a final reward of 978. It first went into (2,1), before turning around and heading for (1,2). With the two hazards marked, it moved for (2,2). At (2,2), it moved into (3,2) as it was already facing east. It then promptly turned back around and headed for (2,3) due to the creaking heard at that position. At (2,3) it happened upon the package, and them beelined it for (1,1).


Reflection:
With this layout, it ran well. However, should there be a damaged floor tile in both (1,3) and (3,1), it would nt be able to complete it's task. The only reason this agent determined that (2,2) was a safe move was because it heard two different danger indicators. If the two danger sounds were the same, the agent would mark (2,2) as a potential hazard, locking itself in a corner. In this case, the robot is unable to prove any tile as safe or unsafe, and the logic is unable to intentionally move onto an unsafe tile. To be fair, with a 66% chance of catching fall to my death disease, I wouldn't chance it either.