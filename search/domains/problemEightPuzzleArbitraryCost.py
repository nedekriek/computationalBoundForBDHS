from .domain import Domains

class problemEightPuzzleArbitraryCost(Domains):
    def __init__(self, initial, goal):
        self.cost_of_actions_used_for_expansion=set()
        initial=tuple((int(loc) %3,int(loc)//3) for loc in initial)
        goal=tuple((int(loc) %3,int(loc)//3) for loc in goal)
        super().__init__(initial, goal)

    def actions(self, state):
        possibleActions=[]
        blankPostion=state[0]
        if blankPostion[0]-1>=0:
            possibleActions.append("LEFT")
        if blankPostion[0]+1<=2:
            possibleActions.append("RIGHT")
        if blankPostion[1]+1<=2:
            possibleActions.append("DOWN")
        if blankPostion[1]-1>=0:
            possibleActions.append("UP")
        return possibleActions

    def result(self, state, action):
        
        if action =="LEFT":
            newBlankPostion=(state[0][0]-1, state[0][1])
        elif action== "RIGHT":
           newBlankPostion=(state[0][0]+1, state[0][1])
        elif action == "DOWN":
            newBlankPostion=(state[0][0], state[0][1]+1)
        elif action == "UP":
            newBlankPostion=(state[0][0], state[0][1]-1)
            
        swapTileIndex=state.index(newBlankPostion)
    
        return (newBlankPostion,)+ state[1:swapTileIndex]+ state[0:1]+ state[swapTileIndex+1:]


    def path_cost(self, c, state1, action, state2):
        newPostionOfBlank=state2[0]
        swappedTile = state1.index(newPostionOfBlank)
        self.cost_of_actions_used_for_expansion.add(swappedTile)
        return c+swappedTile

    


