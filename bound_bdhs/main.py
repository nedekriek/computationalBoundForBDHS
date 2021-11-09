from .constants import run_protocol_definitions, search_pattern
from .utils import  initialiseFile, get_problems

from .generate_nodes import search
from .generate_clauses import clause_generation
from .generate_sat_solution import sat

domain_category = ['pancake']
domain_types=['unit']
run_protocol = [0]
search, constraints, sat = True, False, False

# pancake should always run before eight puzzle as it is quicker
domain_categories = ['pancake', 'eight_puzzle'] if domain_category == [] else domain_category
domain_types = ['unit', 'arbitrary'] if domain_category == [] else domain_types

run_protocol = run_protocol_definitions if run_protocol == [] else [run_protocol_definitions[i] for i in run_protocol]

for domain_category in domain_categories: 
    for domain_type in domain_types:
        problem_set, domain, heuristic = search_pattern[domain_category][domain_type]
        problem_set = get_problems(problem_set)

        paths = ['results/'+domain.__name__+'/search' if search else None,
                 'results/'+domain.__name__+'/constraints' if constraints else None,
                 'results/'+domain.__name__+'/sat' if sat else None]

        for problem in problem_set:
            path_suffix="/"+problem+".obj"
            search_results_path=paths[0]+path_suffix
            if search:
                solution_length, solution_cost = search(domain, heuristic, problem, search_results_path)
            
            for protocol in run_protocol:
                bound_type, bound, locality = protocol

                if constraints:
                    # WARNING IF ONE CLAUSE NEEDS RECUCLATING ALL NEED TO BE RECALCULATED AS THE CONSISTENCY OF VARIABLE NUMBERING MUST BE MAINTAINED
                    avaliable_variable = clause_generation(bound, bound_type, locality, problem, paths[1], search_results_path)

                if sat:
                    