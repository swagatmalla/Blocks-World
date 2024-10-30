# Introducing the Blocks World Problem

The Block World Problem is a classic problem in artificial intelligence and robotics that involves manipulating a set of blocks arranged on a table or in stacks to reach a desired goal configuration. The task models real-world planning and manipulation problems, requiring logical reasoning, sequence planning, and often optimization to achieve the goal. The blocks have specific constraints: only the top block of each stack can be moved, and the blocks must remain on the table or stacked on each other.


# Approach
Operators
An individual block’s state is described by whether  it is clear (it does not have anything on top of it), whether it is in air, and which block it is placed on. The state can be altered by using one of the four operators listed below.
Pickup(X): The pickup operator is applied to a block that is on top of the table. It has two preconditions, the first is that the block is clear or is a pyramid (a pyramid  can always be picked up); the second is that it is not in the air. A picked-up block is assumed to be “in the air”, which can be placed somewhere in the next step.
Putdown(X): The putdown operator is used to set a block on the table. It has one precondition that the block should be in the air.
Stack(X, Y): The stack operator stacks a block X on a block Y. Similar to the pickup operator, stack has two preconditions, the first is that the block to stack on is clear, and the second is that the block being moved is in the air.
Unstack(X, Y). Unstack removes block X that is on top of block Y, where Y is not the table. This operator has the precondition that the block to be unstacked is either clear or a pyramid block.

# Heuristic
A heuristic function is a measure that is used by a search algorithm to determine how to proceed towards a goal. It does that so by assigning a numerical value to a state. A block-world implementation needs a heuristic to “tell” the algorithm how close or far the state is from the goal. In developing our approach, we implemented two different heuristic measures which we then tested on multiple cases and compared for performance. A detailed examination of this comparison is included in the Results section. 

## Heuristic I (Local Maximum)
A simple kind of heuristic measure is to assign a value of (+1) to a block that is on top of a block in a correct position (in reference to the goal state). Otherwise, if the block is on top of a block in an incorrect position, it is assigned a value of (-1). 

## Heuristic II (Global Maximum)

Assign each block a score that is equal to the number of correct blocks underneath it. If one of the blocks is not in the correct position, it is assigned a value of –1*(number of blocks underneath). If a block is in the air or on the table it is assigned a value of (0). Note that the table counts as a block and so a block that is incorrectly placed on the table (instead of say another block where it is supposed to be) is also assigned a value of (-1). This heuristic method has a significant advantage. Instead of assigning a heuristic value to each block relative to the block immediately underneath, it considers the entire structure of a tower in which a block exists. This provides a more accurate representation of the state. For example, in the case of  


