from .domain import Domains

class Domain_eight_puzzle_arbitrary_cost(Domains):
    def __init__(self, initial, goal):
        self.cost_of_actions_used_for_expansion=set()
        initial=tuple((int(loc) %3,int(loc)//3) for loc in initial)
        goal=tuple((int(loc) %3,int(loc)//3) for loc in goal)
        super().__init__(initial, goal)

    def actions(self, state):
        possible_actions=[]
        blank_postion=state[0]
        if blank_postion[0]-1>=0:
            possible_actions.append("LEFT")
        if blank_postion[0]+1<=2:
            possible_actions.append("RIGHT")
        if blank_postion[1]+1<=2:
            possible_actions.append("DOWN")
        if blank_postion[1]-1>=0:
            possible_actions.append("UP")
        return possible_actions

    def result(self, state, action):
        
        if action =="LEFT":
            new_blank_position=(state[0][0]-1, state[0][1])
        elif action== "RIGHT":
           new_blank_position=(state[0][0]+1, state[0][1])
        elif action == "DOWN":
            new_blank_position=(state[0][0], state[0][1]+1)
        elif action == "UP":
            new_blank_position=(state[0][0], state[0][1]-1)
            
        swap_tile_index=state.index(new_blank_position)
    
        return (new_blank_position,)+ state[1:swap_tile_index]+ state[0:1]+ state[swap_tile_index+1:]


    def path_cost(self, c, state1, action, state2):
        new_position_of_blank_postion=state2[0]
        swapped_tile = state1.index(new_position_of_blank_postion)
        self.cost_of_actions_used_for_expansion.add(swapped_tile)
        return c+swapped_tile

    


