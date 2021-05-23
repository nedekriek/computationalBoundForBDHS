from .domain import Domains

class problemPancakeArbitraryCost(Domains):

    def __init__(self, initial, goal):
        self.cost_of_actions_used_for_expansion=set()
        initial=tuple([int(i) for i in initial])
        goal=tuple([int(i) for i in goal])
        super().__init__(initial, goal)     #assumes the goal state is [1,2,3,...,n]

    def actions(self, state):
        """Returns the index of the pancake that is under the flipper. This pancake will not be flipped."""
        possibleActions=[pancakeUnderFlipper for pancakeUnderFlipper in range(2,len(state)+1)]
        return possibleActions

    def result(self, state, action):
        """Given an index directly below the flipper flip the stack."""
        state=list(state)
        flippedPortion=state[0:action]
        flippedPortion.reverse()
        return tuple(flippedPortion + state[action:])

    def path_cost(self, c, state1, action, state2):
        if action == len(state1):
            cost=action+1
        else:           
            cost=state1[action]
        self.cost_of_actions_used_for_expansion.add(cost)
        return c+cost