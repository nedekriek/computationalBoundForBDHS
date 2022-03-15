
from ..search.domains import Domain_eight_puzzle_arbitrary_cost, Domain_eight_puzzle_unit_cost, Domain_pancake_arbitrary_cost, Domain_pancake_unit_cost
from ..search.heuristics import manhattan_arbitrary_cost, manhattan_unit_cost, gap_arbitrary_cost, gap_unit_cost

search_pattern={'eight_puzzle': {'arbitrary': ['computational_bound_for_bdhs/search_problems/sliding_tile/experiment_set.txt', Domain_eight_puzzle_arbitrary_cost,  manhattan_arbitrary_cost ],
                                 'unit': ['computational_bound_for_bdhs/search_problems/sliding_tile/experiment_set.txt',  Domain_eight_puzzle_unit_cost, manhattan_unit_cost]},
                'pancake':{'arbitrary': ['computational_bound_for_bdhs/search_problems/pancake/experiment_set.txt', Domain_pancake_arbitrary_cost, gap_arbitrary_cost],
                           'unit': ['computational_bound_for_bdhs/search_problems/pancake/experiment_set.txt', Domain_pancake_unit_cost, gap_unit_cost]}} 

run_protocol_definitions= [
                           ['front_to_end', 'vc', 'global'],           #front_to_end
                           ['front_to_end', 'lb_minus', 'global'],
                           ['front_to_end', 'lb', 'global'],
                           ['front_to_end', 'ub', 'global'],
                          # ['front_to_end', 'lb_g_limits', 'global'],
                          # ['front_to_end', 'ub_g_limits', 'global'],
                           ['front_to_front', 'vc', 'global'],                      #front_to_front
                           ['front_to_front', 'lb_minus', 'global'],
                           ['front_to_front', 'lb', 'global'],
                           ['front_to_front', 'ub', 'global'],
                          # ['front_to_front', 'lb_g_limits', 'global'],
                          # ['front_to_front', 'ub_g_limits', 'global'],   
                           ['front_to_end', 'vc', 'relative'],                            #front_to_end
                           ['front_to_end', 'lb_minus', 'relative'],
                           ['front_to_end', 'lb', 'relative'],
                           ['front_to_end', 'ub', 'relative'],
                          # ['front_to_end', 'lb_g_limits', 'relative'],
                          # ['front_to_end', 'ub_g_limits', 'relative'],
                           ['front_to_front', 'vc', 'relative'],                      #front_to_front
                           ['front_to_front', 'lb_minus', 'relative'],
                           ['front_to_front', 'lb', 'relative'],
                           ['front_to_front', 'ub', 'relative']
                          # ['front_to_front', 'lb_g_limits', 'relative'],
                          # ['front_to_front', 'ub_g_limits', 'relative']
                          ]

bounds_to_clause={'vc':['must_expand_clauses'],
                  'lb_minus':['must_expand_clauses', 'parent_clauses'],
                  'lb':['must_expand_clauses', 'parent_clauses', 'at_least_one_collision_clauses','might_expand_clauses'],
                  'ub':['not_must_expand_pair_clause', 'parent_clauses', 'no_collision_clauses', 'might_expand_clauses'],
                  'lb_g_limits':['must_expand_clauses', 'parent_clauses', 'at_least_one_collision_clauses','might_expand_clauses', 'g_limit_clauses'],
                  'ub_g_limits':['not_must_expand_pair_clause', 'parent_clauses', 'no_collision_clauses', 'might_expand_clauses', 'g_limit_clauses']
                  }
                 
        #double check the above mapping

# clause_to_bound ={'must_expand_clauses':['vc', 'lb_minus', 'lb', 'lb_g_limits'], TODO: FIX
                #       'parent_clauses':['lb_minus', 'lb', 'ub', 'lb_g_limits', 'ub_g_limits'],
                #       'might_expand_clauses':['lb', 'ub', 'lb_g_limits', 'ub_g_limits'],
                #       'buckets_clauses':['ub', 'ub_g_limits'],
                #       'no_collision_clauses':['ub','ub_g_limits'],
                #       'at_least_one_collision_clauses':['lb', 'lb_g_limits'],
                #       'g_limit_clauses':['lb_g_limits', 'ub_g_limits']}

soft_clause_weight_by_bound_type={'vc':-1,
                                  'lb_minus':-1,
                                  'lb':-1,
                                  'ub':1,
                                  'lb_g_limits':-1,
                                  'ub_g_limits':1}

output_headers = ['problem',
                  'domain_type',
                  'bound',
                  'bound_type',
                  'locality',            
                  'solution_length',
                  'solution_cost',
                  'collision_below_c_star',
                  'max_node_id',
                  'available_variable',
                  'number_of_nodes_set_to_true',
                  'number_of_must_expand_nodes_set_to_true',
                  'bound_value'
                  ]

