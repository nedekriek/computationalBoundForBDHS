import unittest
from ..search.domains.domain_eight_puzzle_unit_cost import Domain_eight_puzzle_unit_cost

class Test_eight_puzzle_unit_cost_problem(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_cases=['602541837_801234567'
                ,'201537468_801234567'
                ,'405132867_801234567'
                ,'031264578_801234567'
                ,'430217568_801234567'
                ,'201563478_801234567'
                ,'701263548_801234567'
                ,'614205837_801234567'
                ,'301247568_801234567'
                ,'230145867_801234567'
                ,'104235867_801234567']
        
        #self.g_values=[6,4,6,4,6,6,5,6,3,6,3]

        goal="801234567"
        self.problem=Domain_eight_puzzle_unit_cost(goal, goal)

    def test_representation(self):
        initial_states=[((0,2),(0,0),(2,0),(2,1),(1,1),(1,0),(2,2),(0,1),(1,2)),
                        ((2,0),(0,0),(1,0),(2,1),(0,1),(1,2),(1,1),(0,2),(2,2)),
                        ((1,1),(0,0),(2,1),(1,0),(0,1),(2,0),(2,2),(0,2),(1,2)),
                        ((0,0),(0,1),(1,0),(2,0),(0,2),(1,1),(2,1),(1,2),(2,2)),
                        ((1,1),(0,1),(0,0),(2,0),(1,0),(1,2),(2,1),(0,2),(2,2)),
                        ((2,0),(0,0),(1,0),(2,1),(0,2),(0,1),(1,1),(1,2),(2,2)),
                        ((1,2),(0,0),(1,0),(2,0),(0,2),(0,1),(2,1),(1,1),(2,2)),
                        ((0,2),(1,0),(1,1),(2,0),(0,0),(2,1),(2,2),(0,1),(1,2)),
                        ((0,1),(0,0),(1,0),(2,0),(1,1),(1,2),(2,1),(0,2),(2,2)),
                        ((2,0),(0,1),(0,0),(1,0),(1,1),(2,1),(2,2),(0,2),(1,2)),
                        ((1,0),(0,0),(1,1),(2,0),(0,1),(2,1),(2,2),(0,2),(1,2))]
        goal_state=((2,2),(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2))

        for index, test_case in enumerate(self.test_cases):
            initial, goal = test_case.split("_")
            problem = Domain_eight_puzzle_unit_cost(initial, goal) 
            self.assertTupleEqual(problem.initial, initial_states[index], "Given initial state "+initial)
            self.assertTupleEqual(problem.goal, goal_state, "Given goal state "+goal)

    def test_possible_actions(self):
        state_and_expected_actions=[(((0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)),["RIGHT","DOWN"]),
                                    (((1,0),(0,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)),["LEFT", "RIGHT","DOWN"]),
                                    (((2,0),(1,0),(0,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)),["LEFT", "DOWN"]),
                                    (((0,1),(1,0),(2,0),(0,0),(1,1),(2,1),(0,2),(1,2),(2,2)), ["RIGHT", "DOWN", "UP"]),
                                    (((1,1),(1,0),(2,0),(0,1),(0,0),(2,1),(0,2),(1,2),(2,2)), ["LEFT","RIGHT", "DOWN", "UP"]),
                                    (((2,1),(1,0),(2,0),(0,1),(1,1),(0,0),(0,2),(1,2),(2,2)), ["LEFT", "DOWN","UP"]),
                                    (((0,2),(1,0),(2,0),(0,1),(1,1),(2,1),(0,0),(1,2),(2,2)), ["RIGHT", "UP"]),
                                    (((1,2),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(0,0),(2,2)), ["LEFT", "RIGHT", "UP",]),
                                    (((2,2),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(0,0)), ["LEFT", "UP"])]
        
        for state, actions in state_and_expected_actions:
            possible_actions=self.problem.actions(state)
            self.assertListEqual(possible_actions, actions, "The state was "+str(state))

    def test_result_of_action(self):
        state=((1,1),(1,0),(2,0),(0,1),(0,0),(2,1),(0,2),(1,2),(2,2))
        action_result= [("UP", ((1,0),(1,1),(2,0),(0,1),(0,0),(2,1),(0,2),(1,2),(2,2))),
                        ("DOWN", ((1,2),(1,0),(2,0),(0,1),(0,0),(2,1),(0,2),(1,1),(2,2))),
                        ("RIGHT", ((2,1),(1,0),(2,0),(0,1),(0,0),(1,1),(0,2),(1,2),(2,2))),
                        ("LEFT", ((0,1),(1,0),(2,0),(1,1),(0,0),(2,1),(0,2),(1,2),(2,2)))]
        for action, result in action_result:
            result_state=self.problem.result(state,action)
            self.assertTupleEqual(result_state, result, "The action was "+ action)

    def test_path_cost(self):
        cost=self.problem.path_cost(5,None,None,None)
        self.assertEqual(cost,6)

if __name__ == '__main__':
    unittest.main()