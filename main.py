import csv
from datetime import datetime

from computational_bound_for_bdhs.bound_bdhs.constants import run_protocol_definitions, search_pattern, output_headers
from computational_bound_for_bdhs.bound_bdhs.utils import get_problems

from computational_bound_for_bdhs.bound_bdhs.generate_nodes import search
from computational_bound_for_bdhs.bound_bdhs.generate_clauses import clause_generation
from computational_bound_for_bdhs.bound_bdhs.generate_sat_solution import sat

# Manual Settings - None if you want everything to run
domain_category = ['pancake']
domain_types=['unit', 'arbitrary']
run_protocol = [0,1,2,3,4,5,6,7]
run_search, run_constraints, run_sat = True, True, True  #Intended options: [[True, True, True],[False, True, True],[False, False, True]]

# pancake should always run before eight puzzle as it is quicker
domain_categories = ['pancake', 'eight_puzzle'] if domain_category == [] else domain_category
domain_types = ['unit', 'arbitrary'] if domain_category == [] else domain_types
run_protocol = run_protocol_definitions if run_protocol == [] else [run_protocol_definitions[i] for i in run_protocol]

for domain_category in domain_categories: 
    for domain_type in domain_types:
        problem_set, domain, heuristic = search_pattern[domain_category][domain_type]
        problem_set = get_problems(problem_set)

        paths = ['results/'+domain.__name__+'/search' if run_search else None,  #if not exists(search_results_path):
                 'results/'+domain.__name__+'/constraints' if run_constraints else None,
                 'results/'+domain.__name__+'/sat' if run_sat else None,
                 'results/'+domain.__name__+'/']

        version = datetime.now().strftime('date_%d_%m_%y_time_%H_%M')
        csv_file = open(paths[3]+'results_'+version+'.csv', "w")
        writer=csv.writer(csv_file)
        writer.writerow(output_headers)


        for problem in problem_set:
            path_suffix="/"+problem+".obj"
            search_results_path=paths[0]+path_suffix

            bound = '-'
            bound_type = '-'
            locality = '-'            
            solution_length = '-'
            solution_cost = '-'
            collision_below_c_star = '-'
            max_node_id = '-'
            available_variable = '-'
            number_of_nodes_set_to_true = '-'
            number_of_must_expand_nodes_set_to_true = '-'

            if run_search:
                solution_length, solution_cost, max_node_id = search(domain, heuristic, problem, search_results_path)
                with open(paths[0]+"/"+problem+".txt","w") as f:
                    f.write("{},{},{}".format(solution_length, solution_cost, max_node_id))
            else:
                with open(paths[0]+"/"+problem+".txt","r") as f:
                    line = f.readline()
                    solution_length, solution_cost, max_node_id = [int(item) for item in line.split(',')]
            
            for protocol in run_protocol:
                bound_type, bound, locality = protocol
                bound_constraints_path_prefix = paths[1]+'/'+bound+'/'+bound_type+'/'+locality+'/'

                if run_constraints:
                    # WARNING IF ONE CLAUSE NEEDS RECUCLATING ALL NEED TO BE RECALCULATED AS THE CONSISTENCY OF VARIABLE NUMBERING MUST BE MAINTAINED
                    available_variable, collision_below_c_star = clause_generation(heuristic, bound, bound_type, locality, problem, bound_constraints_path_prefix, path_suffix, search_results_path)
                    with open(bound_constraints_path_prefix+problem+".txt","w") as f:
                        f.write("{},{}".format(available_variable, collision_below_c_star))
                else:
                    with open(bound_constraints_path_prefix+problem+".txt","r") as f:
                        line = f.readline()
                        available_variable, collision_below_c_star = [int(item) for item in line.split(',')]   
                    
                if run_sat:
                   sat_path = paths[2]+'/'+bound+'/'+bound_type+'/'+locality

                   number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true = sat(collision_below_c_star, max_node_id, bound, bound_type, sat_path, path_suffix, bound_constraints_path_prefix)

                writer.writerow([problem,
                                 bound,
                                 bound_type,
                                 locality,            
                                 solution_length,
                                 solution_cost,
                                 collision_below_c_star,
                                 max_node_id,
                                 available_variable,
                                 number_of_nodes_set_to_true,
                                 number_of_must_expand_nodes_set_to_true,
                                 number_of_nodes_set_to_true +1 if not collision_below_c_star and bound in ('ub', 'ub_g_limits') else number_of_nodes_set_to_true
                                 ]
                                 )
        csv_file.close()

                
 