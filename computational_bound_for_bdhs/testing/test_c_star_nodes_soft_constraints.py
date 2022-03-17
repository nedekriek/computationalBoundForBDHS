import unittest

from ..search.domains.Eight_puzzle_unit import Eight_puzzle_unit
from ..search.unidirectional_search.node import Node

from aStar.experiments import Experiment

class Test_constraints(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        self.closed_list_forward_2=dict()
        self.closed_list_backward_2=dict()
        self.solution_nodes_forward_2=[]
        self.solution_nodes_backward_2=[]
    
        self.experiment_2=Experiment("unitTest", Eight_puzzle_unit, None, None, "unitTests/test.txt")
        self.experiment_2.max_node_id=12
        self.experiment_2.epsilon_global=1
        self.experiment_2.iota_global=1

        parent_action_pairs_forward_2=[("a", (None, None)), ("b", ("a", "A")), ("c", ("a", "B")), ("d", ("c", "C")), ("e", ("d", "E"))] 
        parent_action_pairs_backward_2=[("e", (None, None)), ("f", ("e", "E")), ("d", ("e", "D")), ("c", ("d", "C")), ("a", ("c", "B"))]

        #Node values (g,h,f,b,d)
        node_values_forward_2={"a":(0,3,3,0,3), "b":(1,2,3,0,3), "c":(1,2,3,0,3), "d":(2,1,3,0,3), "e":(3,0,3,0,3)}
        node_values_backward_2={"e":(0,3,3,0,3), "f":(1,2,3,0,3), "d":(1,2,3,0,3), "c":(2,1,3,0,3), "a":(3,0,3,0,3)}
        
        for state, parent_action_pairs in parent_action_pairs_forward_2:
            parent, action = parent_action_pairs
            node=Node(state, self.closed_list_forward_2[parent] if parent != None else None, action, node_values_forward_2[state][0])
            self.closed_list_forward_2[state]=node

        for state, parent_action_pairs in parent_action_pairs_backward_2:
            parent, action = parent_action_pairs
            node=Node(state, self.closed_list_backward_2[parent]if parent != None else None, action, node_values_backward_2[state][0])
            self.closed_list_backward_2[state]=node

        for state, (g, h, f, b, d) in node_values_forward_2.items():
            node=self.closed_list_forward_2[state]
            setattr(node, "h", h)
            setattr(node, "f", f)
            setattr(node, "b", b)
            setattr(node, "d", d)

        for state, (g, h, f, b, d) in node_values_backward_2.items():
            node=self.closed_list_backward_2[state]
            setattr(node, "h", h)
            setattr(node, "f", f)
            setattr(node, "b", b)
            setattr(node, "d", d)

        self.solution_nodes_forward_2.append(self.closed_list_forward_2["e"])
        self.solution_nodes_backward_2.append(self.closed_list_backward_2["a"])

        self.closed_list_forward_3=dict()
        self.closed_list_backward_3=dict()
        self.solution_nodes_forward_3=[]
        self.solution_nodes_backward_3=[]
        Node.count=1

        parent_action_pairs_forward_3 = [("a", (None, None)), ("b", ("a", "A")), ("c", ("a", "B")), ("d", ("c", "C")), ("e", ("d", "E")),("g", ("c", "F")), ("h", ("d", "G"))] 
        parent_action_pairs_backward_3 = [("e", (None, None)), ("f", ("e", "E")), ("d", ("e", "D")), ("c", ("d", "C")), ("a", ("c", "B")), ("g", ("c", "F")), ("h", ("d", "G"))]

         #Node values (g,h,f,d,b)
        node_values_forward_3={"a":(0,3,3,0,3), "c":(2,2,4,1,5), "d":(4,1,5,2,7), "e":(6,0,6,3,9), "b":(1,5,6,0,6), "g":(3,2,5,2,7), "h": (5,1,6,2,8)}
        node_values_backward_3={"e":(0,3,3,0,3), "d":(2,1,3,1,4), "c":(4,1,5,1,6), "a":(6,0,6,2,8), "f":(1,5,6,0,6), "g":(5,1,6,2,8), "h":(3,1,4,2,6)}
    
        self.experiment_3=Experiment("unitTest", Eight_puzzle_unit, None, None, "unitTests/test.txt")
        self.experiment_3.max_node_id=12
        self.experiment_3.epsilon_global=1
        self.experiment_3.iota_global=1

        for state, parent_action_pairs in parent_action_pairs_forward_3:
            parent, action = parent_action_pairs
            node=Node(state, self.closed_list_forward_3[parent] if parent != None else None, action, node_values_forward_3[state][0])
            self.closed_list_forward_3[state]=node

        for state, parent_action_pairs in parent_action_pairs_backward_3:
            parent, action = parent_action_pairs
            node=Node(state, self.closed_list_backward_3[parent]if parent != None else None, action, node_values_backward_3[state][0])
            self.closed_list_backward_3[state]=node

        for state, (g, h, f, d, b) in node_values_forward_3.items():
            node=self.closed_list_forward_3[state]
            setattr(node, "h", h)
            setattr(node, "f", f)
            setattr(node, "b", b)
            setattr(node, "d", d)

        for state, (g, h, f, d, b) in node_values_backward_3.items():
            node=self.closed_list_backward_3[state]
            setattr(node, "h", h)
            setattr(node, "f", f)
            setattr(node, "b", b)
            setattr(node, "d", d)

        self.solution_nodes_forward_3.append(self.closed_list_forward_3["e"])
        self.solution_nodes_backward_3.append(self.closed_list_backward_3["a"])

    def test_c_star_nodes_on_optimal_path_only(self):
        soft_constraints, hard_constraints = self.experiment_2.minimise_nodes(self.solution_nodes_forward_2, self.solution_nodes_backward_2, self.closed_list_forward_2, self.closed_list_backward_2)
        expected_soft_constraints=[self.closed_list_forward_2["a"].id, self.closed_list_forward_2["c"].id, self.closed_list_forward_2["d"].id,self.closed_list_forward_2["e"].id,
                                    self.closed_list_backward_2["a"].id, self.closed_list_backward_2["c"].id, self.closed_list_backward_2["d"].id,self.closed_list_backward_2["e"].id]
        expected_hard_constraints=[]

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints)
        
    def test_collision_below_c_star(self):
        soft_constraints, hard_constraints = self.experiment_3.maximise_nodes(self.solution_nodes_forward_3, self.solution_nodes_backward_3, self.closed_list_forward_3, self.closed_list_backward_3)
        expected_soft_constraints = [self.closed_list_forward_3["a"].id, self.closed_list_forward_3["c"].id, self.closed_list_forward_3["d"].id, self.closed_list_forward_3["g"].id,
                                     self.closed_list_backward_3["c"].id, self.closed_list_backward_3["d"].id,self.closed_list_backward_3["e"].id, self.closed_list_backward_3["h"].id]
        expected_hard_constraints = []

        self.assertIsInstance(soft_constraints, list)
        self.assertIsInstance(hard_constraints, list)

        self.assertCountEqual(soft_constraints, expected_soft_constraints)
        self.assertCountEqual(hard_constraints, expected_hard_constraints) 

if __name__ == '__main__':
    unittest.main()