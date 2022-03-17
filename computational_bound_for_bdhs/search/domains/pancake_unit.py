from .domain import Domain

class Pancake_unit(Domain):

    def __init__(self, initial, goal): 
        self.epsilon_global = 1
        self.iota_global = 1
        initial=tuple([int(i) for i in initial]+[len(initial)+1]) # [len(initial)+1] adds the table to the state
        goal=tuple([int(i) for i in goal]+[len(initial)+1])
        super().__init__(initial, goal)     #assumes the goal state is [1,2,3,...,n]

    def actions(self, state):
        """Returns the index of the pancake that is under the flipper. This pancake will not be flipped."""
        possible_actions=[pancake_under_flipper for pancake_under_flipper in range(2,len(state))]
        return possible_actions

    def result(self, state, action):
        """Given an index directly below the flipper flip the stack."""
        state=list(state)
        flipped_portion=state[0:action]
        flipped_portion.reverse()
        return tuple(flipped_portion + state[action:])

    def path_cost(self, c, state1, action, state2):
        return c+1
