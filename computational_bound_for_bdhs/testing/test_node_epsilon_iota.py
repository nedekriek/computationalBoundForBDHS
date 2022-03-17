import unittest
import sys
sys.path.append("..")

from ..search.domains.Pancake_unit import Pancake_unit
from ..search.domains.Pancake_arbitrary import Pancake_arbitrary

from ..search.domains.Eight_puzzle_unit import Eight_puzzle_unit
from ..search.domains.Eight_puzzle_arbitrary import Eight_puzzle_arbitrary
from ..search.unidirectional_search.node import Node

class Test_epsilon_iota(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.eight_puzzle_state=((1,1),(0,0),(1,0),(2,0),(0,1),(0,2),(2,1),(2,2),(1,2))
        self.eight_puzzle_actions=["LEFT","RIGHT", "DOWN", "UP"]

        self.pancake_state=[1,4,2,3,5]
        self.pancake_actions=[2,3,4,5]
        return
    
    def test_unit_cost(self):
        eight_puzzle_problem=Eight_puzzle_unit("123456780","012345678")
        node=Node(self.eight_puzzle_state)
        children=node.expand(eight_puzzle_problem)
        self.assertEquals(node.epsilon, 1, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        self.assertEquals(node.iota, 1, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        
        pancake_problem=Pancake_unit("32541","12345")
        node=Node(self.pancake_state)
        children=node.expand(pancake_problem)
        self.assertEquals(node.epsilon, 1, "The problem is pancake with state "+str(self.pancake_state))
        self.assertEquals(node.iota, 1, "The problem is pancake with state "+str(self.pancake_state))
    
    def test_epsilon_arbitrary_cost(self):
        eight_puzzle_problem=Eight_puzzle_arbitrary("123456780","012345678")
        node=Node(self.eight_puzzle_state)
        children=node.expand(eight_puzzle_problem)
        self.assertEquals(node.epsilon, 2, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        self.assertEquals(node.iota, 2, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        
        pancake_problem=Pancake_arbitrary("32541","12345")
        node=Node(self.pancake_state)
        children=node.expand(pancake_problem)
        self.assertEquals(node.epsilon, 2, "The problem is pancake with state "+str(self.pancake_state))
        self.assertEquals(node.iota, 1, "The problem is pancake with state "+str(self.pancake_state))

if __name__ == '__main__':
    unittest.main()