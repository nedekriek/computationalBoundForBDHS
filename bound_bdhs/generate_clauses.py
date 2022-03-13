from os.path import exists

from .constants import clause_to_bound
from .utils import serialize, deserialize


#clauses
#from ..clause_generation_helper.bucket_clauses import buckets_clauses
from ..clause_generation_helper.expand_clauses import must_expand_clauses
from ..clause_generation_helper.perantage_clauses import parentage_clauses
from ..clause_generation_helper.colision_clauses import get_collision_locations, no_collision_clauses, at_least_one_collision_clauses
from ..clause_generation_helper.g_limit_clauses import g_limit_clauses

#clause utils
from ..clause_generation_helper.utils import buckets, visible_search_space, static_front_to_end_lb, static_front_to_front_lb, dynamic_front_to_end_lb, dynamic_front_to_front_lb,  solution_is_below_c_star


def clause_generation(heuristic_function, bound: str, bound_type: str, locality: str, problem: str, bound_constraints_path_prefix: str, path_suffix: str, search_path: str):
    '''
    Generates all clauses for a search problem given a bound, its' type and locality eg. (lb_nx, front_to_front, global).

    Clauses included:
        - must_expand_clauses
        - parent_clauses
        - buckets_clauses
        - g_limit_clauses
        - no_collision_clauses
        - at_least_one_collision_clauses
    '''
    required_clauses=clause_to_bound[bound]

    requires_recalculation=False  

    for clause_type in required_clauses:
        path=bound_constraints_path_prefix+clause_type+'/'+path_suffix
        # If any clause type is missing recalculate all clauses as there are 2 groups of highly dependent clauses for which numbering needs to stay consistant
        if not exists(path):                        
            requires_recalculation=True
            break

    # WARNING IF ONE CLAUSE NEEDS RECUCLATING ALL NEED TO BE RECALCULATED AS THE CONSISTENCY OF VARIABLE NUMBERING MUST BE MAINTAINED IN THE HIGHLY DEPENDANT CLAUSE GROUPS
    if requires_recalculation:
        max_node_id, epsilon_global, iota_global, solution_nodes_f, solution_nodes_b, closed_list_f, closed_list_b = deserialize(search_path+problem+".obj")
        avaliable_variable=max_node_id+1    #every method assumes that the available variable passed to it has not been used in any other clause and is not a node id
        c_star = solution_nodes_f[0].g
        global_info = True if locality == 'global' else False
        static_node_lower_bound_func = static_front_to_end_lb if bound_type == 'front_to_end' else static_front_to_front_lb
        dynamic_node_lower_bound_func = dynamic_front_to_end_lb if bound_type == 'front_to_end' else dynamic_front_to_front_lb
        heuristic_function = heuristic_function if bound_type == 'front_to_front' else None
        # Begin clause genration

        # Dependant set 1
        buckets_f = buckets(closed_list_f, epsilon_global, iota_global, global_info)
        buckets_b = buckets(closed_list_b, epsilon_global, iota_global, global_info)
        must_expand_paired_buckets, might_expand_paired_buckets = visible_search_space(static_node_lower_bound_func, buckets_f, buckets_b, c_star)

        must_expand_pairs, might_expand_pairs, not_must_expand_pair_clause = must_expand_clauses(dynamic_node_lower_bound_func, heuristic_function, must_expand_paired_buckets, might_expand_paired_buckets, buckets_f, buckets_b, bound_type,  c_star, epsilon_global, iota_global, global_info, avaliable_variable)
        serialize(must_expand_pairs, bound_constraints_path_prefix+'must_expand_clauses/'+path_suffix)
        must_expand_pairs = []
        serialize(might_expand_pairs, bound_constraints_path_prefix+'might_expand_pairs/'+path_suffix)
        might_expand_pairs = []
        serialize(not_must_expand_pair_clause, bound_constraints_path_prefix+'not_must_expand_pair_clause/'+path_suffix)
        not_must_expand_pair_clause = []

        parentage = parentage_clauses(might_expand_paired_buckets, must_expand_paired_buckets, buckets_f, buckets_b)
        serialize(parentage, bound_constraints_path_prefix+'parent_clauses/'+path_suffix)
        parentage = []        

        # bucket_aliases_f, bucket_aliases_b, avaliable_variable, bucket = buckets_clauses(might_expand_paired_buckets, must_expand_paired_buckets, buckets_f, buckets_b, avaliable_variable)
        # serialize(bucket, bound_constraints_path_prefix+'buckets_clauses/'+path_suffix)
        # bucket = []

        avaliable_variable, gLimit = g_limit_clauses(bucket_aliases_f, bucket_aliases_b,  c_star, epsilon_global, avaliable_variable)
        serialize(gLimit, bound_constraints_path_prefix+'g_limit_clauses/'+path_suffix)
        gLimit = []

        # Clean up
        buckets_f = []
        buckets_b = []
        must_expand_paired_buckets = []
        might_expand_paired_buckets = []
        bucket_aliases_f = []
        bucket_aliases_b = []

        # Dependant set 2
        common_child_collisions, nodes_adjacent_to_terminal = get_collision_locations(solution_nodes_f, solution_nodes_b, closed_list_b)

        no_collision = no_collision_clauses(common_child_collisions, nodes_adjacent_to_terminal)
        serialize(no_collision, bound_constraints_path_prefix+'no_collision_clauses/'+path_suffix)
        no_collision = []

        avaliable_variable , at_least_one_collision = at_least_one_collision_clauses(common_child_collisions, nodes_adjacent_to_terminal, avaliable_variable)
        serialize(at_least_one_collision, bound_constraints_path_prefix+'at_least_one_collision_clauses/'+path_suffix)
        at_least_one_collision = []

        # Clean up
        common_child_collisions = []
        nodes_adjacent_to_terminal = []

        collision_below_c_star = solution_is_below_c_star(dynamic_node_lower_bound_func, heuristic_function, solution_nodes_f, closed_list_b, c_star, epsilon_global, iota_global, global_info)

        return avaliable_variable, collision_below_c_star
    return None