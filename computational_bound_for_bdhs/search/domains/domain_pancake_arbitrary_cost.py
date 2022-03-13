from .domain import Domain

class Domain_pancake_arbitrary_cost(Domain):

    def __init__(self, initial, goal):
        self.cost_of_actions_used_for_expansion=set()
        initial=tuple([int(i) for i in initial])
        goal=tuple([int(i) for i in goal])
        super().__init__(initial, goal)     #assumes the goal state is [1,2,3,...,n]

    def actions(self, state):
        """Returns the index of the pancake that is under the flipper. This pancake will not be flipped."""
        possible_actions=[pancake_under_flipper for pancake_under_flipper in range(2,len(state)+1)]
        return possible_actions

    def result(self, state, action):
        """Given an index directly below the flipper flip the stack."""
        state=list(state)
        flipped_portion=state[0:action]
        flipped_portion.reverse()
        return tuple(flipped_portion + state[action:])

    def path_cost(self, c, state1, action, state2):
        if action == len(state1):
            cost=action+1
        else:           
            cost=state1[action]
        self.cost_of_actions_used_for_expansion.add(cost)
        return c+cost