from ..search.unidirectional_search.a_star_search import a_star_search
from ..search.unidirectional_search.node import Node
from ..search.unidirectional_search.post_process_b_and_d_values import post_process
from .serialization import serialize
from .utils import getIndex

import os
from math import gcd
from functools import reduce

class SearchOnly:
    def __init__(self, heuristic, problem_type, problem_list):
        self.problem_type=problem_type
        self.heuristic=heuristic
        self.index= getIndex(problem_list)
        self.search_dir="results/searchResults/"
        self.current_solution_length=None
    
    def initialiseDir(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def search(self, case):
        initial_state, goal_state = case.split("_")

        forward = self.problem_type(initial_state, goal_state)
        backward = self.problem_type(goal_state, initial_state)
        solution_nodes_forward, closed_list_forward = a_star_search(forward, self.heuristic)  
        solution_nodes_backward, closed_list_backward = a_star_search(backward, self.heuristic)

        maxNodeId = Node.count
        Node.count=1                #The counter must be reset for ever (intail_state, goal_state) pair for correct and efficient encoding

        if forward.cost_of_actions_used_for_expansion:
            forwardEpsilon=min(forward.cost_of_actions_used_for_expansion) 
            forwardIota=reduce(gcd, forward.cost_of_actions_used_for_expansion)
            backwardEpsilon=min(backward.cost_of_actions_used_for_expansion)
            backwardIota=reduce(gcd,backward.cost_of_actions_used_for_expansion)
            global_epsilon=min(forwardEpsilon,backwardEpsilon)
            global_iota=reduce(gcd,[forwardIota,backwardIota])
        else:
            global_epsilon=0
            global_iota=0

        #calculate d and b values
        post_process(closed_list_forward, closed_list_backward, self.heuristic, forward)

        self.current_solution_length=solution_nodes_forward[0].g 
        data=[maxNodeId, global_epsilon, global_iota, solution_nodes_forward, solution_nodes_backward, closed_list_forward, closed_list_backward]
        return data

    def run(self):
        self.initialiseDir(self.search_dir+"/"+self.problem_type.__name__)
        self.initialiseDir(self.search_dir+"/"+self.problem_type.__name__+"/"+self.heuristic.__name__)
        solution_lengths_file="results/solution_lengths/"+self.problem_type.__name__+"/"+self.heuristic.__name__+"/"+self.problem_list+".txt"
        
        for case in self.index:
            data=self.search(case)
            serialize(data, self.search_dir+"/"+self.problem_type.__name__+"/"+self.heuristic.__name__+"/"+case+".obj")
            
            line=case+","+str(self.current_solution_length)
            file_object=open(solution_lengths_file, "a")
            file_object.write("{}\n".format(line))
            file_object.close()

