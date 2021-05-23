import unittest
import sys
sys.path.append("..")

from ..search.domains.domain_pancake_unit_cost import Domain_pancake_unit_cost
from ..search.domains.domain_pancake_arbitrary_cost import Domain_pancake_arbitrary_cost

from ..search.domains.domain_eight_puzzle_unit_cost import Domain_eight_puzzle_unit_cost
from ..search.domains.domain_eight_puzzle_arbitrary_cost import Domain_eight_puzzle_arbitrary_cost
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
        eight_puzzle_problem=Domain_eight_puzzle_unit_cost("123456780","012345678")
        node=Node(self.eight_puzzle_state)
        children=node.expand(eight_puzzle_problem)
        self.assertEquals(node.epsilon, 1, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        self.assertEquals(node.iota, 1, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        
        pancake_problem=Domain_pancake_unit_cost("32541","12345")
        node=Node(self.pancake_state)
        children=node.expand(pancake_problem)
        self.assertEquals(node.epsilon, 1, "The problem is pancake with state "+str(self.pancake_state))
        self.assertEquals(node.iota, 1, "The problem is pancake with state "+str(self.pancake_state))
    
    def test_epsilon_arbitrary_cost(self):
        eight_puzzle_problem=Domain_eight_puzzle_arbitrary_cost("123456780","012345678")
        node=Node(self.eight_puzzle_state)
        children=node.expand(eight_puzzle_problem)
        self.assertEquals(node.epsilon, 2, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        self.assertEquals(node.iota, 2, "The problem is 8 puzzle with state "+str(self.eight_puzzle_state))
        
        pancake_problem=Domain_pancake_arbitrary_cost("32541","12345")
        node=Node(self.pancake_state)
        children=node.expand(pancake_problem)
        self.assertEquals(node.epsilon, 2, "The problem is pancake with state "+str(self.pancake_state))
        self.assertEquals(node.iota, 1, "The problem is pancake with state "+str(self.pancake_state))

if __name__ == '__main__':
    unittest.main()