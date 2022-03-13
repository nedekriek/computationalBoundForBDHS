import unittest
import sys
sys.path.append("..")

from  ..search.heuristics.manhattan_distance import manhattan_unit_cost, manhattan_arbitrary_cost
from  ..search.unidirectional_search.node import Node

class TestEightPuzzleHeuristics(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_states=[((0,2),(0,0),(2,0),(2,1),(1,1),(1,0),(2,2),(0,1),(1,2)),  #602541837
                        ((2,0),(0,0),(1,0),(2,1),(0,1),(1,2),(1,1),(0,2),(2,2)),    #201537468
                        ((1,1),(0,0),(2,1),(1,0),(0,1),(2,0),(2,2),(0,2),(1,2)),    #405132867
                        ((0,0),(0,1),(1,0),(2,0),(0,2),(1,1),(2,1),(1,2),(2,2)),    #031264578
                        ((1,1),(0,1),(0,0),(2,0),(1,0),(1,2),(2,1),(0,2),(2,2)),    #430217568
                        ((2,0),(0,0),(1,0),(2,1),(0,2),(0,1),(1,1),(1,2),(2,2)),    #201563478
                        ((1,2),(0,0),(1,0),(2,0),(0,2),(0,1),(2,1),(1,1),(2,2)),    #701263548
                        ((0,2),(1,0),(1,1),(2,0),(0,0),(2,1),(2,2),(0,1),(1,2)),    #614205837
                        ((0,1),(0,0),(1,0),(2,0),(1,1),(1,2),(2,1),(0,2),(2,2)),    #301247568
                        ((2,0),(0,1),(0,0),(1,0),(1,1),(2,1),(2,2),(0,2),(1,2)),    #230145867
                        ((1,0),(0,0),(1,1),(2,0),(0,1),(2,1),(2,2),(0,2),(1,2))]    #104235867
        self.goal=((2,2),(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2))

        self.manhattan_distance=[(0,1,1,1,1,1,1,0),
                                (0,0,1,0,1,1,0,1),
                                (0,2,1,0,2,1,0,0),
                                (1,0,0,1,0,0,1,1),
                                (1,1,0,2,1,0,0,1),
                                (0,0,1,1,1,1,1,1),
                                (0,0,0,1,1,0,2,1),
                                (1,1,0,1,1,1,1,0),
                                (0,0,0,1,1,0,0,1),
                                (1,1,1,1,1,1,0,0),
                                (0,1,0,0,1,1,0,0)]

    def test_unit_cost(self):
        for index, case in enumerate(self.test_states):
            expected_h_value=sum(self.manhattan_distance[index])
            node=Node(case)
            h_value=manhattan_unit_cost(node, self.goal)
            self.assertEqual(h_value, expected_h_value, "The state was "+str(case))

    def test_arbitrary_cost(self):
        for index, case in enumerate(self.test_states):
            expected_h_value=0
            manhattan_distance=self.manhattan_distance[index]
            for weight in range(1,9):
                expected_h_value+= weight*manhattan_distance[weight-1]
            node=Node(case)
            h_value=manhattan_arbitrary_cost(node, self.goal)
            self.assertEqual(h_value, expected_h_value, "The state was "+str(case))

if __name__ == '__main__':
    unittest.main()