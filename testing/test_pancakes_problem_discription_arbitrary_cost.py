import unittest
import sys
sys.path.append("..")

from ..search.domains.domain_pancake_arbitrary_cost import Domain_pancake_arbitrary_cost

class Test_pancakes_arbitrary_cost_problem(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.problem=Domain_pancake_arbitrary_cost("123", "123")

    def test_representation(self):
        test_inputs_outputs=[("123 123", (1,2,3), (1,2,3)),
                            ("132 123", (1,3,2), (1,2,3)),
                            ("213 123", (2,1,3), (1,2,3))]

        for inputs, expected_initial, expected_goal in test_inputs_outputs:
            inputs = inputs.split()
            problem = Domain_pancake_arbitrary_cost(inputs[0],inputs[1])
            self.assertTupleEqual(problem.initial, expected_initial)
            self.assertTupleEqual(problem.goal, expected_goal)

    def test_possible_actions(self):
        test_problem_state_actions=[([1,2,3,4,5,6,7],[2,3,4,5,6,7]),
                                    ([5,2,1,3,4],[2,3,4,5]),
                                    ([2,4,1,3,5],[2,3,4,5]),
                                    ([3,5,4,1,2],[2,3,4,5]),
                                    ([3,1,2], [2,3]),
                                    ([2,1,3], [2,3]),
                                    ([1,2], [2])]
                
        for state, expected_actions in test_problem_state_actions:
            actions= self.problem.actions(state)
            self.assertListEqual(actions, expected_actions, "The test state is "+str(state))

    def test_result_of_action(self):
        state_action_result=[([5,2,1,3,4],2,(2,5,1,3,4)),
                            ([5,2,1,3,4],3,(1,2,5,3,4)),
                            ([5,2,1,3,4],4,(3,1,2,5,4)),
                            ([5,2,1,3,4],5,(4,3,1,2,5)),
                            ([3,1,2],2,(1,3,2)),
                            ([3,1,2],3,(2,1,3)),
                            ([1,2],2,(2,1))]
        
        for state, action, expected_result in state_action_result:
            result=self.problem.result(state,action)
            self.assertTupleEqual(result, expected_result)
            
    def test_path_cost(self):
        state_action_result=[((7,6,5,4,2,1,3),7,8),
                            ((5,2,1,3,4),5,6),
                            ((2,4,1,3,5),3,3),
                            ((3,5,4,1,2),4,2),
                            ((3,1,2),3,4),
                            ((2,1,3),2,3),
                            ((1,2),2,3)]
        for state, action, expected_result in state_action_result:
            cost=self.problem.path_cost(0,state,action,None)
            self.assertEqual(cost,expected_result, "The test state was "+str(state)+" the test action was "+str(action))

        
if __name__ == '__main__':
    unittest.main()