import unittest
import sys
sys.path.append("..")

from  ..search.heuristics.gap_heuristic import gap_unit_cost, gap_arbitrary_cost
from  ..search.unidirectional_search.node import Node

class TestPancakeHeuristics(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_cases=["2314 1234",
                        "2341 1234",
                        "2413 1234",
                        "34521 12345",
                        "35124 12345",
                        "35142 12345"]
        self.gap=[2,1,3,1,3,4]
        self.arbitrary_gap=[2,1,4,2,6,7]

    def test_unit_cost(self):
        for index, case in enumerate(self.test_cases):
            initial,goal =case.split()
            initial=[int(i) for i in initial]
            goal=[int(g) for g in goal]
            node=Node(initial)
            cost=gap_unit_cost(node, goal)
            expected_cost=self.gap[index]
            self.assertEqual(cost, expected_cost, "The test case is "+str(initial)+" with goal "+str(goal))

    def test_arbitrary_cost(self):
        for index, case in enumerate(self.test_cases):
            initial,goal =case.split()
            initial=[int(i) for i in initial]
            goal=[int(g) for g in goal]
            node=Node(initial)
            cost=gap_arbitrary_cost(node, goal)
            expected_cost=self.arbitrary_gap[index]
            self.assertEqual(cost, expected_cost, "The test case is "+str(initial)+" with goal "+str(goal))


if __name__ == '__main__':
    unittest.main()