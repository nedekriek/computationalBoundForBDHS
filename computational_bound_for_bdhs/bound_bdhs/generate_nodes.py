from functools import reduce
from genericpath import exists
from ..search.unidirectional_search.a_star_search import a_star_search
from ..search.unidirectional_search.node import Node
from ..search.unidirectional_search.post_process_b_and_d_values import post_process
from .utils import serialize 
from math import gcd
from functools import reduce


def search(domain, heuristic, problem: str, search_results_path: str):
    if not exists(search_results_path):
        initial_state, goal_state = problem.split("_")

        problem_f=domain(initial_state, goal_state)
        problem_b=domain(goal_state,initial_state)

        solution_nodes_f, closed_list_f = a_star_search(problem_f, heuristic)  
        solution_nodes_b, closed_list_b = a_star_search(problem_b, heuristic)

        max_node_id = Node.count
        Node.count = 1                #The counter must be reset for every (intail_state, goal_state) pair for correct and efficient encoding

        if problem_f.cost_of_actions_used_for_expansion:
            epsilon_f=min(problem_f.cost_of_actions_used_for_expansion)
            iota_f=reduce(gcd, problem_f.cost_of_actions_used_for_expansion)
            epsilon_b=min(problem_b.cost_of_actions_used_for_expansion)
            iota_b=reduce(gcd, problem_b.cost_of_actions_used_for_expansion)

            epsilon_global=min(epsilon_f,epsilon_b)
            iota_global=reduce(gcd,[iota_f,iota_b])
        else: # only free actions taken
            epsilon_global=0  
            iota_global=0
        
        post_process(closed_list_f, closed_list_b, heuristic, problem_f)  

        solution_cost=solution_nodes_f[0].g 
        solution_length=solution_nodes_f[0].solution_length()

        serialize([max_node_id, epsilon_global, iota_global, solution_nodes_f, solution_nodes_b, closed_list_f, closed_list_b ], search_results_path)
        
        return solution_length, solution_cost, max_node_id
    return None, None