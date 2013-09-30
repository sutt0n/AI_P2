from search import *
import utils
import copy

#define our solution state
# _____________
# |   |   |   |
# | 1 | 2 | 3 |
# |___|___|___|
# |   |   |   |
# | 4 | 5 | 6 |
# |___|___|___|
# |   |   |   |
# | 7 | 8 |   |
# |___|___|___|
solutionState = [ [1,2,3], [4,5,6], [7,8,0] ]

# Define the position where each block is supposed to be on the board
goalPositions = {
        1 : (0,0),
        2 : (0,1),
        3 : (0,2),
        4 : (1,0),
        5 : (1,1),
        6 : (1,2),
        7 : (2,0),
        8 : (2,1),
        0 : (2,2)
}

# Define the actions you can take on the 0-tile
up = "up"
down = "down"
left = "left"
right = "right"

class EightTileProblem(GraphProblem):
    def __init__(self, initialState, goalState, startNode):
        Problem.__init__(self, initialState, goalState)
        self.graph = startNode
        
    # Define the heuristic that will be used in the A* search 
    def h(self, node):
        """h function for the current node is the sum of the Manhattan Distance
        of each block in the current node's state to its destination -- that is,
        the x distance difference plus the y difference distance"""
        sum = 0
        for rowNumber, rowArray in enumerate(node.state):
            for colNumber, blockValue in enumerate(rowArray):
                sum += manhattanDistance(goalPositions[blockValue], (rowNumber, colNumber))
        return sum
    
    # Define the actions we can take on the "0 tile" to swap it
    def actions(self, A): # A is a state
        "The actions at a graph node are just its neighbors."
        "You can either go left, right, up, or down, if the bounds allow it"
        # Find the 0-tile's position
        for rowNumber, rowArray in enumerate(A):
            for colNumber, blockValue in enumerate(rowArray):
                if blockValue == 0:
                    zeroRow = rowNumber
                    zeroCol = colNumber
                    break
                #else:
                #    print "checking node block [", rowNumber, ",", colNumber, "] with value ", blockValue
        results = []
        # Swap whichever vertical neighbors you can
        if zeroRow == 0: # swap with the one beneath it            
            results.append(down);
        elif zeroRow == 2: # swap with the one above it
            results.append(up);
        else: # Otherwise, you can do top and bottom
            results.append(up);
            results.append(down);
        
        # Swap whichever vertical neighbors you can
        if zeroCol == 0: # swap with the one right of it
            results.append(right);
        elif zeroCol == 2: # swap with the one left of it
            results.append(left);
        else: # Otherwise, you can do left and right
            results.append(left);
            results.append(right);
        
        # DEBUG
        """
        print "possible results for ", A
        for result in results:
            print result, " "
        print ""
        """
        return results
    
    # The result of swapping the 0-tile with another tile is a new state
    # Note that result() returns a "state", which is passed to the Node constructor
    # (see child_node() in the Node class)
    def result(self, state, action):
        for rowNumber, rowArray in enumerate(state):
            for colNumber, blockValue in enumerate(rowArray):
                if blockValue == 0:
                    zRow = rowNumber
                    zCol = colNumber
                    break
                
        # Make a deep copy so as not to alter the original Node 
        childState = copy.deepcopy(state)
        
        if action == up:
            # this is how you execute a swap()
            childState[zRow][zCol], childState[zRow-1][zCol] = childState[zRow-1][zCol], childState[zRow][zCol]
            return childState
        elif action == down:
            childState[zRow][zCol], childState[zRow+1][zCol] = childState[zRow+1][zCol], childState[zRow][zCol]
            return childState
        elif action == left:
            childState[zRow][zCol], childState[zRow][zCol-1] = childState[zRow][zCol-1], childState[zRow][zCol]
            return childState
        elif action == right:
            childState[zRow][zCol], childState[zRow][zCol+1] = childState[zRow][zCol+1], childState[zRow][zCol]
            return childState
        else:
            return "Woops, invalid action"
        
    # Path cost is always 1 in this problem    
    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + 1
    
    def __repr__(self):
        """ TODO: Change to be purdy. """
        return "<Node %s>" % (self.state,)

sInit = [[1,2,3],[0,5,6],[4,7,8]]
nStart = Node(sInit) 
gpEightTile = EightTileProblem(sInit, solutionState, nStart)
print breadth_first_tree_search(gpEightTile).solution()