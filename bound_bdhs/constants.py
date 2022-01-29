
from ..search.domains import Domain_eight_puzzle_arbitrary_cost, Domain_eight_puzzle_unit_cost, Domain_pancake_arbitrary_cost, Domain_pancake_unit_cost
from ..search.heuristics import manhattan_arbitrary_cost, manhattan_unit_cost, gap_arbitrary_cost, gap_unit_cost

search_pattern={'eight_puzzle': {'arbitrary': ['search_problems/sliding_tile/experiment_set.txt', Domain_eight_puzzle_arbitrary_cost,  manhattan_arbitrary_cost ],
                                 'unit': ['search_problems/sliding_tile/experiment_set.txt',  Domain_eight_puzzle_unit_cost, manhattan_unit_cost]},
                'pancake':{'arbitrary': ['search_problems/pancake/experiment_set.txt', Domain_pancake_arbitrary_cost, gap_arbitrary_cost],
                           'unit': ['search_problems/pancake/experiment_set.txt', Domain_pancake_unit_cost, gap_unit_cost]}} 

run_protocol_definitions= [['front_to_back', 'vc_g_mx', 'global'],           #front_to_back
                           ['front_to_back', 'lb_minus_nx', 'global'],
                           ['front_to_back', 'lb_nx', 'global'],
                           ['front_to_back', 'ub_nx', 'global'],
                           ['front_to_back', 'lb_nx_with_g_limits', 'global'],
                           ['front_to_back', 'ub_nx_with_g_limits', 'global'],
                           ['front_to_front', 'vc_g_mx', 'global'],                      #front_to_front
                           ['front_to_front', 'lb_minus_nx', 'global'],
                           ['front_to_front', 'lb_nx', 'global'],
                           ['front_to_front', 'ub_nx', 'global'],
                           ['front_to_front', 'lb_nx_with_g_limits', 'global'],
                           ['front_to_front', 'ub_nx_with_g_limits', 'global'],   
                           ['front_to_back', 'vc_g_mx', 'relative'],           #front_to_back
                           ['front_to_back', 'lb_minus_nx', 'relative'],
                           ['front_to_back', 'lb_nx', 'relative'],
                           ['front_to_back', 'ub_nx', 'relative'],
                           ['front_to_back', 'lb_nx_with_g_limits', 'relative'],
                           ['front_to_back', 'ub_nx_with_g_limits', 'relative'],
                           ['front_to_front', 'vc_g_mx', 'relative'],                      #front_to_front
                           ['front_to_front', 'lb_minus_nx', 'relative'],
                           ['front_to_front', 'lb_nx', 'relative'],
                           ['front_to_front', 'ub_nx', 'relative'],
                           ['front_to_front', 'lb_nx_with_g_limits', 'relative'],
                           ['front_to_front', 'ub_nx_with_g_limits', 'relative']]

bounds_to_clause={'vc_g_mx':['must_expand_clauses'],
                 'lb_minus_nx':['must_expand_clauses', 'parent_clauses'],
                 'lb_nx':['must_expand_clauses', 'parent_clauses', 'at_least_one_collision_clauses','visible_search_space_clauses'],
                 'ub_nx':['buckets_clauses', 'parent_clauses', 'no_collision_clauses', 'visible_search_space_clauses'],
                 'lb_nx_with_g_limits':['must_expand_clauses', 'parent_clauses', 'at_least_one_collision_clauses','visible_search_space_clauses', 'g_limit_clauses'],
                 'ub_nx_with_g_limits':['buckets_clauses', 'parent_clauses', 'no_collision_clauses', 'visible_search_space_clauses', 'g_limit_clauses']}
        #double check the above mapping

clause_to_bound ={'must_expand_clauses':['vc_g_mx', 'lb_minus_nx', 'lb_nx', 'lb_nx_with_g_limits'],
                      'parent_clauses':['lb_minus_nx', 'lb_nx', 'ub_nx', 'lb_nx_with_g_limits', 'ub_nx_with_g_limits'],
                      'visible_search_space_clauses':['lb_nx', 'ub_nx', 'lb_nx_with_g_limits', 'ub_nx_with_g_limits'],
                      'buckets_clauses':['ub_nx', 'ub_nx_with_g_limits'],
                      'no_collision_clauses':['ub_nx','ub_nx_with_g_limits'],
                      'at_least_one_collision_clauses':['lb_nx', 'lb_nx_with_g_limits'],
                      'g_limit_clauses':['lb_nx_with_g_limits', 'ub_nx_with_g_limits']}

soft_clause_weight_by_bound_type={'vc_g_mx':-1,
                                  'lb_minus_nx':-1,
                                  'lb_nx':-1,
                                  'ub_nx':1,
                                  'lb_nx_with_g_limits':-1,
                                  'ub_nx_with_g_limits':1}

output_headers = ['problem',
                  'bound',
                  'bound_type',
                  'locality',            
                  'solution_length',
                  'solution_cost',
                  'collision_below_c_star',
                  'max_node_id',
                  'avaliable_variable',
                  'number_of_nodes_set_to_true',
                  'number_of_must_expand_nodes_set_to_true',
                  ]

