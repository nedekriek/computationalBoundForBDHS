import csv
from datetime import datetime
import functools
from tqdm import tqdm

from computational_bound_for_bdhs.bound_bdhs.constants import run_protocol_definitions, search_pattern, output_headers
from computational_bound_for_bdhs.bound_bdhs.utils import get_problems

from computational_bound_for_bdhs.bound_bdhs.generate_nodes import search
from computational_bound_for_bdhs.bound_bdhs.generate_clauses import clause_generation
from computational_bound_for_bdhs.bound_bdhs.generate_sat_solution import sat

# Manual Settings - None if you want everything to run
domain_category = ['pancake']
domain_types= []
run_protocol = [2,3,6,7]
run_search, run_constraints, run_sat = True, True, True  #Intended options: [[True, True, True],[False, True, True],[False, False, True]]

# pancake should always run before eight puzzle as it is quicker
domain_categories = ['pancake', 'eight_puzzle'] if domain_category == [] else domain_category
domain_types = ['unit', 'arbitrary'] if domain_types == [] else domain_types
run_protocol = run_protocol_definitions if run_protocol == [] else [run_protocol_definitions[i] for i in run_protocol]

degradation=0

for domain_category in domain_categories: 
    for domain_type in domain_types:
        problem_set, domain, base_heuristic = search_pattern[domain_category][domain_type]
        heuristic = functools.partial(base_heuristic, degradation=degradation)
        problem_set = get_problems(problem_set)

        paths = ['results/'+domain.__name__+'/search/d'+str(degradation) if run_search else None,  #
                 'results/'+domain.__name__+'/constraints/d'+str(degradation) if run_constraints else None,
                 'results/'+domain.__name__+'/sat/d'+str(degradation) if run_sat else None,
                 'results/'+domain.__name__+'/d'+str(degradation)+'/']


        # paths = ['results/'+domain.__name__+'/search' if run_search else None,  #if not exists(search_results_path):
        #          'results/'+domain.__name__+'/constraints' if run_constraints else None,
        #          'results/'+domain.__name__+'/sat' if run_sat else None,
        #          'results/'+domain.__name__+'/']

        version = datetime.now().strftime('date_%d_%m_%y_time_%H_%M')
        csv_file = open(paths[3]+version+'degradation_'+str(degradation)+'.csv', "w") #add degradation to filename - Pat

        writer=csv.writer(csv_file)
        writer.writerow(output_headers)


        for problem in tqdm(problem_set):
            path_suffix="/"+problem+".obj"
            search_results_path=paths[0]+path_suffix
            search_data_path = paths[0]+"/"+problem+".txt"

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
                solution_length, solution_cost, max_node_id = search(domain, heuristic, problem, search_results_path, search_data_path)
                with open(search_data_path,"w") as f:
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
                                 domain_type,
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
                                 number_of_nodes_set_to_true +1 if bound in ('ub', 'ub_g_limits') and number_of_nodes_set_to_true is not None else number_of_nodes_set_to_true
                                 ]
                                 )
        csv_file.close()

                
 

# import csv
# from datetime import datetime
# from tqdm import tqdm

# from computational_bound_for_bdhs.bound_bdhs.constants import run_protocol_definitions, search_pattern, output_headers
# from computational_bound_for_bdhs.bound_bdhs.utils import get_problems

# from computational_bound_for_bdhs.bound_bdhs.generate_nodes import search
# from computational_bound_for_bdhs.bound_bdhs.generate_clauses import clause_generation
# from computational_bound_for_bdhs.bound_bdhs.generate_sat_solution import sat

# # Manual Settings - None if you want everything to run
# domain_category = ['pancake']
# domain_types= []
# run_protocol = [2,3,6,7]
# run_search, run_constraints, run_sat = True, True, True  #Intended options: [[True, True, True],[False, True, True],[False, False, True]]

# # pancake should always run before eight puzzle as it is quicker
# domain_categories = ['pancake', 'eight_puzzle'] if domain_category == [] else domain_category
# domain_types = ['unit', 'arbitrary'] if domain_types == [] else domain_types
# run_protocol = run_protocol_definitions if run_protocol == [] else [run_protocol_definitions[i] for i in run_protocol]

# degradation=0

# for domain_category in domain_categories: 
#     for domain_type in domain_types:
#         problem_set, domain, heuristic = search_pattern[domain_category][domain_type]
#         problem_set = get_problems(problem_set)

#         paths = ['results/'+domain.__name__+'/search/d'+str(degradation) if run_search else None,  #
#                  'results/'+domain.__name__+'/constraints/d'+str(degradation) if run_constraints else None,
#                  'results/'+domain.__name__+'/sat/d'+str(degradation) if run_sat else None,
#                  'results/'+domain.__name__+'/d'+str(degradation)+'/']

#         version = datetime.now().strftime('date_%d_%m_%y_time_%H_%M')
#         csv_file = open(paths[3]+'results_'+version+'.csv', "w")
#         writer=csv.writer(csv_file)
#         writer.writerow(output_headers)


#         for problem in tqdm(problem_set):
#             path_suffix="/"+problem+".obj"
#             search_results_path=paths[0]+path_suffix

#             bound = '-'
#             bound_type = '-'
#             locality = '-'            
#             solution_length = '-'
#             solution_cost = '-'
#             collision_below_c_star = '-'
#             max_node_id = '-'
#             available_variable = '-'
#             number_of_nodes_set_to_true = '-'
#             number_of_must_expand_nodes_set_to_true = '-'

#             if run_search:
#                 solution_length, solution_cost, max_node_id = search(domain, heuristic, problem, search_results_path)
#                 with open(search_results_path,"w") as f:
#                     f.write("{},{},{}".format(solution_length, solution_cost, max_node_id))
#             else:
#                 with open(search_results_path,"r") as f:
#                     line = f.readline()
#                     solution_length, solution_cost, max_node_id = [int(item) for item in line.split(',')]
            
#             for protocol in run_protocol:
#                 bound_type, bound, locality = protocol
#                 bound_constraints_path_prefix = paths[1]+'/'+bound+'/'+bound_type+'/'+locality+'/'

#                 if run_constraints:
#                     # WARNING IF ONE CLAUSE NEEDS RECUCLATING ALL NEED TO BE RECALCULATED AS THE CONSISTENCY OF VARIABLE NUMBERING MUST BE MAINTAINED
#                     available_variable, collision_below_c_star = clause_generation(heuristic, bound, bound_type, locality, problem, bound_constraints_path_prefix, path_suffix, search_results_path)
#                     with open(bound_constraints_path_prefix+problem+".txt","w") as f:
#                         f.write("{},{}".format(available_variable, collision_below_c_star))
#                 else:
#                     with open(bound_constraints_path_prefix+problem+".txt","r") as f:
#                         line = f.readline()
#                         available_variable, collision_below_c_star = [int(item) for item in line.split(',')]   
                    
#                 if run_sat:
#                     sat_path = paths[2]+'/'+bound+'/'+bound_type+'/'+locality

#                     number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true = sat(collision_below_c_star, max_node_id, bound, bound_type, sat_path, path_suffix, bound_constraints_path_prefix)

#                 writer.writerow([problem,
#                                  domain_type,
#                                  bound,
#                                  bound_type,
#                                  locality,            
#                                  solution_length,
#                                  solution_cost,
#                                  collision_below_c_star,
#                                  max_node_id,
#                                  available_variable,
#                                  number_of_nodes_set_to_true,
#                                  number_of_must_expand_nodes_set_to_true,
#                                  number_of_nodes_set_to_true +1 if bound in ('ub', 'ub_g_limits') and number_of_nodes_set_to_true is not None else number_of_nodes_set_to_true
#                                  ]
#                                  )
#         csv_file.close()

                
 
