import unittest
import sys
sys.path.append("..")

from computational_bound_for_bdhs.search.heuristics.gap_heuristic import gap_unit_cost, gap_arbitrary_cost
from computational_bound_for_bdhs.search.unidirectional_search.node import Node

class TestPancakeHeuris5tics(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_cases=["2314 1234",
                        "2341 1234",
                        "2413 1234",
                        "34521 12345",
                        "35124 12345",
                        "35142 12345"]
        self.gap=[2,2,4,2,4,5]
        self.arbitrary_gap=[4,5,10,7,14,15]

    def test_unit_cost(self):
        for index, case in enumerate(self.test_cases):
            initial,goal =case.split()
            initial=tuple([int(i) for i in initial]+[len(goal)+1])
            goal=tuple([int(g) for g in goal]+[len(goal)+1])
            node=Node(initial)
            cost=gap_unit_cost(node, goal, degradation=0)
            expected_cost=self.gap[index]
            self.assertEqual(cost, expected_cost, "The test case is "+str(initial)+" with goal "+str(goal))

    def test_arbitrary_cost(self):
        for index, case in enumerate(self.test_cases):
            initial,goal =case.split()
            initial=tuple([int(i) for i in initial]+[len(goal)+1])
            goal=tuple([int(g) for g in goal]+[len(goal)+1])
            node=Node(initial)
            cost=gap_arbitrary_cost(node, goal, degradation=0)
            expected_cost=self.arbitrary_gap[index]
            self.assertEqual(cost, expected_cost, "The test case is "+str(initial)+" with goal "+str(goal))


if __name__ == '__main__':
    unittest.main()