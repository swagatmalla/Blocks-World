from state import State
import itertools
import copy
from queue import PriorityQueue
import time

class Plan:

    def __init__(self, initial_state, goal_state):
        """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type initial_state: list of block.Block objects
        """
        self.initial_state = initial_state
        self.goal_state = goal_state

    def pickup(self, block1):
        """
        Operator to pickup the block from the table
        :param block1: block1 to pick up from the table
        :type block1: Object of block.Block
        :return: None
        """
        # if block1.type == 2:

        #     block1.air = True
        #     block1.on = None

        if (block1.clear or block1.type == 2) and not block1.air:
            block1.unclear()
            block1.air = True
            block1.on = None

    def putdown(self, block1):
        """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

        # get table object from initial state
        table = State.find(self.initial_state, "table")

        if block1.air:
            block1.on = table
            block1.clear = True
            block1.air = False
            if block1.type == 2: block1.clear = False

    def stack(self, block1, block2):
        """
        Operator to stack block1 onto block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """
        if block1.air and block2.clear: #block 1 is in air and 2 does not have anything on top
            block1.air = False #We placed in on block2, no longer in air
            block1.on = block2 #place it on block2
            block2.unclear()
            if block1.type != 2: 
                block1.clear = True

    def unstack(self, block1, block2):
        """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

        # if block1 is clear safe to unstack
        if block1.clear or block1.type == 2:

            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.clear = False
            block1.air = True
            block1.on = None

            block2.clear = True    

    def neighbors(self, currentState):
        cleartoLiftBlocks = [] #blocks that don't have anything on top, which includes the pyramid
        blocksinAir = [] #block that is in air
        neighborList = []

        for block in currentState[1::]:
            if block.air:
                blocksinAir.append(block)
        
        #if len(blocksinAir) > 1 : print("!!!SOMETHING  BROKE. THERE CAN'T BE MORE THAN 1 BLOCK IN AIR")

        for block in currentState[1::]:             #finding blocks that can be lifted up. This includes the pyramid
            if block.clear or block.type == 2:
                cleartoLiftBlocks.append(block)

        #print("Blocks that are clear: ", cleartoLiftBlocks)
        #print("Block that is in the air ", blocksinAir) 

        #If nothing is in the air then all we can do is either pickup or unstack
        if len(blocksinAir) == 0 :
            for block in cleartoLiftBlocks:
                if block.on.id == 'table':
                    neighborState = copy.deepcopy(currentState)
                    index = [b.id for b in neighborState].index(block.id)
                    blocktoPickup = neighborState[index]
                    
                    self.pickup(blocktoPickup)
                    action = f"Pickup({blocktoPickup})"
                    neighborList.append([action, neighborState])
                    #State.display(neighborState, message = action)
                else:
                    #if the block is not on the table
                    neighborState = copy.deepcopy(currentState)
                    index = [b.id for b in neighborState].index(block.id)
                    blocktoUnstack = neighborState[index]
                    index = [b.id for b in neighborState].index(block.on.id)
                    unStackfrom = neighborState[index]
                
                    self.unstack(blocktoUnstack, unStackfrom)
                    action = f"Unstack({blocktoUnstack}) from {unStackfrom}"

                    neighborList.append([action, neighborState])
                    #State.display(neighborState, message = action)

        else: #if something is in the air, we can either put it down on the table or stack it somewhere
            
            #Just putting it down on the table
            neighborState = copy.deepcopy(currentState)
            index = [b.id for b in neighborState].index(blocksinAir[0].id)
            blocktoPutdown = neighborState[index]
            action = f"Putdown({blocktoPutdown} on the table)"
            self.putdown(blocktoPutdown)
            
            neighborList.append([action, neighborState])
            #State.display(neighborState, message = action)

            #Stack it somewhere viable
            looper = iter(cleartoLiftBlocks) #[1::] because we don't want the table
            currBlock = next(looper)
            while True: 
                try:
                    if currBlock.clear:
                        neighborState = copy.deepcopy(currentState)
                        blocktoStack = neighborState[[b.id for b in neighborState].index(blocksinAir[0].id)]
                        stackonTopOf = neighborState[[b.id for b in neighborState].index(currBlock.id)]

                        action = f"Stack({blocktoStack}) on {stackonTopOf}"
                        self.stack(blocktoStack,stackonTopOf)
                        
                        neighborList.append([action, neighborState])
                       #State.display(neighborState, message = action)

                    currBlock = next(looper)
                except StopIteration:
                    break
        return neighborList

        
    def h1(currentState, goalState): #in this approach we will assign a block +1 if it is on top of the correct block, 0 otherwise (local maximum)
        score = 0
        for index in range(1, len(goalState.blocks)):
            if currentState.blocks[index].on == goalState.blocks[index].on:
                score += 1
        return score

    def h2(self, currentState, goalState): 
        #a global maximum 
        #if correct support structure, assign a block score equal to the number of correct blocks underneath the current one; 
        #if the support structure underneath is not correct, assign a score of -1 *(number of incorrect blocks underneath) 
        score = 0
        for i in range(1, len(goalState)):
            #print(goalState[i])
            if currentState[i].air:
                continue
            goalStructure = []
            currentStructure = []

            onTopOf = goalState[i].on
            onTopOf2 = currentState[i].on
            #print(f"on top of {onTopOf}")
            goalStructure.append(onTopOf)
            currentStructure.append(onTopOf2)

            while not onTopOf.id == 'table':
                if onTopOf.on != None: onTopOf = onTopOf.on
                #print(onTopOf)
                goalStructure.append(onTopOf)

            while not onTopOf2.id == 'table':
                if onTopOf2.on != None: onTopOf2 = onTopOf2.on
                #print(onTopOf)
                currentStructure.append(onTopOf2)
            
            #print(f"Goal Structure for {goalState[i].id} {goalStructure}")
            #print()
            #print(f"Current Structure for {currentState[i].id} {currentStructure}")
            #print()
          
            if not currentStructure[0].id == 'table':
                if [block.id for block in currentStructure] == [block.id for block in goalStructure]:
                    score += len(currentStructure) -1
                else:
                    score -= 1 * (len(currentStructure) - 1)
        
        #print('----------------------------------------------------------------------')        
        return(score)
            
        

    def hasVisited(self,currState, visitedStates):
        hasVisited = True
        for state in visitedStates:
            i = 1 #start from 1 because we don't care about the table
            for block in state[1::]:
                if currState[i].on != block.on:  
                        hasVisited = False
                        break
                else:
                    hasVisited = True
                i += 1
            if hasVisited: return True
        
        return False

    def plan(self):
        #greedy best first search
        counter = 0 # to count the number of unique steps
        frontier = PriorityQueue()
        currState = ["Initial State",initial_state.blocks]
        goalState = goal_state.blocks
        visitedStates = []
        frontier.put((-1 *self.h2(currState[1], goalState), currState))
        visitedStates.append(currState[1])
        targetHeuristic = -1 * self.h2(goalState, goalState)
        while not frontier.empty() and (-1*self.h2(currState[1], goalState)) !=  targetHeuristic:
            neighbors = self.neighbors(currState[1]) 
            for neighbor in neighbors:
                if not self.hasVisited(neighbor[1], visitedStates):
                    frontier.put((-1*self.h2(neighbor[1], goalState), neighbor))
                    visitedStates.append(neighbor[1])   
            currState = frontier.get()[1]
            #print("Current H val: ", self.h2(currState[1], goalState))

            State.display(currState[1], message = currState[0])
            counter += 1
        print(f"Number of unique steps: {counter}")
    

if __name__ == "__main__":

    # get the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")
    #print("Initial state blocks ",initial_state_blocks)

    #display initial state
    State.display(initial_state_blocks, message = "Initial State")

    # get the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")

    #display goal state
    State.display(goal_state_blocks, message = "Goal State")


    p = Plan(initial_state_blocks, goal_state_blocks)
    start = time.time()
    p.plan()
    end = time.time()
    print(f"It took {end - start} seconds")






