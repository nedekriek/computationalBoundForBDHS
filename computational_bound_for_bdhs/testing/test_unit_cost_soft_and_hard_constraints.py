import unittest
from array import array
import sys
sys.path.append("..")

from ..search.domains.Eight_puzzle_unit import Eight_puzzle_unit
from ..search.unidirectional_search.node import Node
from aStar.experiments import Experiment


class Test_constraints(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        self.closed_list_forward_1=dict()
        self.closed_list_backward_1=dict()
        self.solution_nodes_forward_1=[]
        self.solution_nodes_backward_1=[]

        parent_action_pairs_forward=[("a",[(None,None)]), ("b",[("a","A")]), ("c",[("a","B")]), ("d",[("a","C")]),
                                    ("e",[("b","D")]), ("f",[("c","E"), ("d","F")]), ("g",[("d","G")]),
                                    ("h",[("f","H")]), ("i",[("f","I"), ("g", "J")]), ("j",[("h","L"),("i","k")])]
        parent_action_pairs_backward=[("j",[(None,None)]), ("k",[("j","M")]),("h",[("j","L")]), ("i",[("j","K")]),
                                    ("l",[("k","N")]), ("f",[("h","H"), ("i", "H")]), ("g",[("i","J")]),
                                    ("c",[("f","E")]), ("d",[("f","F"), ("g", "G")]), ("a",[("c","B"), ("d","C")])]

        forward_g_values={"a":0, "b":1, "c":1, "d":1, "e":2, "f":2, "g":2, "h":3, "i":3, "j":4}
        backward_g_values={"a":4, "c":3, "d":3, "f":2, "g":2, "l":2, "h":1, "i":1, "k":1, "j":0}    
        
        forward_h_values={"a":3, "b":2, "c":2, "d":2, "e":1, "f":1, "g":1, "h":0, "i":0, "j":0}  #"l":2, "k":1} included for notational perposes only
        backward_h_values={"a":0, "c":0, "d":0, "f":1, "g":1, "l":1, "h":2, "i":2, "k":2, "j":3} #"b":1, "e":2} 
        
        forward_b_values={"a":4, "b":3, "c":4, "d":4, "e":3, "f":4, "g":4, "h":4, "i":4, "j":4}
        backward_b_values={"a":4, "c":4, "d":4, "f":4, "g":4, "l":3, "h":4, "i":4, "k":3, "j":4} 
        
        forward_d_values={"a":0, "b":0, "c":1, "d":1, "e":0, "f":1, "g":1, "h":1, "i":1, "j":1}
        backward_d_values={"a":1, "c":3, "d":1, "f":1, "g":1, "l":0, "h":1, "i":1, "k":0, "j":0}  

        for state, parent_action_pairs in parent_action_pairs_forward:
            parent, action = parent_action_pairs.pop()
            node=Node(state, self.closed_list_forward_1[parent] if parent != None else None, action, forward_g_values[state])
            if len(parent_action_pairs)>0:
                for pair in parent_action_pairs:
                    node.append_parent_action_pair((self.closed_list_forward_1[pair[0]], pair[1]))
            self.closed_list_forward_1[state]=node

        for state, parent_action_pairs in parent_action_pairs_backward:
            parent, action = parent_action_pairs.pop()
            node=Node(state, self.closed_list_backward_1[parent]if parent != None else None, action, backward_g_values[state])
            if len(parent_action_pairs)>0:
                for pair in parent_action_pairs:
                    node.append_parent_action_pair((self.closed_list_backward_1[pair[0]], pair[1]))
            self.closed_list_backward_1[state]=node
        
        for state, node in self.closed_list_forward_1.items():
            setattr(node, "h", forward_h_values[state])
            setattr(node, "f", self.closed_list_forward_1[state].g+self.closed_list_forward_1[state].h)
            setattr(node, "b", forward_b_values[state])
            setattr(node, "d", forward_d_values[state])

        for state, node in self.closed_list_backward_1.items():
            setattr(node, "h", backward_h_values[state])
            setattr(node, "f", self.closed_list_backward_1[state].g+self.closed_list_backward_1[state].h)
            setattr(node, "b", backward_b_values[state])
            setattr(node, "d", backward_d_values[state])
        
        self.solution_nodes_forward_1.append(self.closed_list_forward_1["j"])
        self.solution_nodes_backward_1.append(self.closed_list_backward_1["a"])
    
        self.experiment=Experiment("unitTest", problemEightPuzzleUnitCost, None, None, "unitTests/test.txt")
        self.experiment.max_node_id=20
        self.experiment.epsilon_global=1
        self.experiment.iota_global=1

    def test_must_expand_pairs(self):
        soft_constraints, hard_constraints = self.experiment.must_expand_pairs(self.solution_nodes_forward_1, self.solution_nodes_backward_1, self.closed_list_forward_1, self.closed_list_backward_1)
        expected_soft_constraints = [self.closed_list_forward_1["b"].id, self.closed_list_backward_1["k"].id]
        expected_hard_constraints = [array("q", [self.closed_list_forward_1["b"].id, self.closed_list_backward_1["k"].id])]

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints)

    def test_parents(self):
        soft_constraints, hard_constraints = self.experiment.parents(self.solution_nodes_forward_1, self.solution_nodes_backward_1, self.closed_list_forward_1, self.closed_list_backward_1)
        expected_hard_constraints = [array("q", [self.closed_list_forward_1["a"].id, -1*self.closed_list_forward_1["b"].id]),
                                    array("q", [self.closed_list_forward_1["a"].id, -1*self.closed_list_forward_1["c"].id]),
                                    array("q", [self.closed_list_forward_1["a"].id, -1*self.closed_list_forward_1["d"].id]),
                                    array("q", [self.closed_list_forward_1["b"].id, -1*self.closed_list_forward_1["e"].id]),
                                    array("q", [self.closed_list_forward_1["d"].id, self.closed_list_forward_1["c"].id, -1*self.closed_list_forward_1["f"].id]),
                                    array("q", [self.closed_list_forward_1["d"].id, -1*self.closed_list_forward_1["g"].id]),
                                    array("q", [self.closed_list_forward_1["f"].id, -1*self.closed_list_forward_1["h"].id]),
                                    array("q", [self.closed_list_forward_1["g"].id, self.closed_list_forward_1["f"].id, -1*self.closed_list_forward_1["i"].id]),
                                    array("q", [self.closed_list_forward_1["i"].id, self.closed_list_forward_1["h"].id, -1*self.closed_list_forward_1["j"].id]),

                                    array("q", [self.closed_list_backward_1["j"].id, -1*self.closed_list_backward_1["k"].id]),
                                    array("q", [self.closed_list_backward_1["k"].id, -1*self.closed_list_backward_1["l"].id]),
                                    array("q", [self.closed_list_backward_1["j"].id, -1*self.closed_list_backward_1["i"].id]),
                                    array("q", [self.closed_list_backward_1["j"].id, -1*self.closed_list_backward_1["h"].id ]),
                                    array("q", [self.closed_list_backward_1["i"].id, self.closed_list_backward_1["h"].id, -1*self.closed_list_backward_1["f"].id]),
                                    array("q", [self.closed_list_backward_1["i"].id, -1*self.closed_list_backward_1["g"].id]),
                                    array("q", [self.closed_list_backward_1["f"].id, -1*self.closed_list_backward_1["c"].id]),
                                    array("q", [self.closed_list_backward_1["g"].id, self.closed_list_backward_1["f"].id, -1*self.closed_list_backward_1["d"].id]),
                                    array("q", [self.closed_list_backward_1["d"].id, self.closed_list_backward_1["c"].id,  -1*self.closed_list_backward_1["a"].id ])]
        expected_soft_constraints = []

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints)


    def test_at_least_one_collision(self):
        soft_constraints, hard_constraints = self.experiment.at_least_one_collision(self.solution_nodes_forward_1, self.solution_nodes_backward_1, self.closed_list_forward_1, self.closed_list_backward_1)
        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        collision_ids=[21,22,23,24,25,26,27,28]
        expected_dummy_variables_and_singles=array("q", collision_ids+[self.closed_list_forward_1["h"].id, self.closed_list_forward_1["i"].id, self.closed_list_backward_1["c"].id, self.closed_list_backward_1["d"].id])
        expected_pairs=[(self.closed_list_forward_1["a"].id, self.closed_list_backward_1["f"].id),
                        (self.closed_list_forward_1["a"].id, self.closed_list_backward_1["g"].id),
                        (self.closed_list_forward_1["c"].id, self.closed_list_backward_1["h"].id),
                        (self.closed_list_forward_1["c"].id, self.closed_list_backward_1["i"].id),
                        (self.closed_list_forward_1["d"].id, self.closed_list_backward_1["h"].id),
                        (self.closed_list_forward_1["d"].id, self.closed_list_backward_1["i"].id),
                        (self.closed_list_forward_1["f"].id, self.closed_list_backward_1["j"].id),
                        (self.closed_list_forward_1["g"].id, self.closed_list_backward_1["j"].id),]

        collision_pairs=hard_constraints[:16]
        pairs=[]
        dummy_variables=[]
        expected_dummy_variables=[-21,-22,-23,-24,-25,-26,-27,-28]
        for index in range(0, len(collision_pairs),2):
            self.assertEqual(collision_pairs[index][0], collision_pairs[index+1][0])
            dummy_variables.append(collision_pairs[index][0])
            pairs.append((collision_pairs[index][1], collision_pairs[index+1][1]))

        self.assertCountEqual(dummy_variables, expected_dummy_variables)
        self.assertCountEqual(pairs, expected_pairs)

        dummy_variables_and_singles=hard_constraints[16:][0]
        self.assertCountEqual(dummy_variables_and_singles, expected_dummy_variables_and_singles)

        expected_soft_constraints = []
        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        

    def test_no_collision(self):
        soft_constraints, hard_constraints = self.experiment.no_collision(self.solution_nodes_forward_1, self.solution_nodes_backward_1, self.closed_list_forward_1, self.closed_list_backward_1)
        expected_soft_constraints = []
        expected_hard_constraints = [array("q", [-1*self.closed_list_forward_1["a"].id, -1*self.closed_list_backward_1["f"].id]),
                                    array("q", [-1*self.closed_list_forward_1["a"].id, -1*self.closed_list_backward_1["g"].id]),
                                    array("q", [-1*self.closed_list_forward_1["c"].id, -1*self.closed_list_backward_1["h"].id]),
                                    array("q", [-1*self.closed_list_forward_1["c"].id, -1*self.closed_list_backward_1["i"].id]),
                                    array("q", [-1*self.closed_list_forward_1["d"].id, -1*self.closed_list_backward_1["h"].id]),
                                    array("q", [-1*self.closed_list_forward_1["d"].id, -1*self.closed_list_backward_1["i"].id]),
                                    array("q", [-1*self.closed_list_forward_1["f"].id, -1*self.closed_list_backward_1["j"].id]),
                                    array("q", [-1*self.closed_list_forward_1["g"].id, -1*self.closed_list_backward_1["j"].id]),
                                    array("q", [-1*self.closed_list_forward_1["h"].id]), array("q",[-1*self.closed_list_forward_1["i"].id]),
                                    array("q", [-1*self.closed_list_backward_1["c"].id]), array("q",[-1*self.closed_list_backward_1["d"].id])]

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints) 

    def test_minimise_nodes(self):
        soft_constraints, hard_constraints = self.experiment.minimise_nodes(self.solution_nodes_forward_1, self.solution_nodes_backward_1, self.closed_list_forward_1, self.closed_list_backward_1)
        expected_soft_constraints = [node.id for node in list(self.closed_list_forward_1.values()) + list(self.closed_list_backward_1.values())]
        expected_hard_constraints = []

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints) 

    def test_maximise_nodes(self):
        soft_constraints, hard_constraints = self.experiment.maximise_nodes(self.solution_nodes_forward_1, self.solution_nodes_backward_1, self.closed_list_forward_1, self.closed_list_backward_1)
        expected_soft_constraints = [node.id for node in list(self.closed_list_forward_1.values()) + list(self.closed_list_backward_1.values())]
        expected_hard_constraints = []

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints) 


if __name__ == '__main__':
    unittest.main()