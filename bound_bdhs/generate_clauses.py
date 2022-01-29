from os.path import exists

from .constants import bounds
from .utils import serialize, deserialize


#clauses
from ..clause_generation_helper.bucket_clauses import buckets_clauses
from ..clause_generation_helper.must_expand_clauses import must_expand_clauses
from ..clause_generation_helper.perantage_clauses import parentage_clauses
from ..clause_generation_helper.bucket_clauses import get_collision_locations, no_collision_clauses, at_least_one_collision_clauses
from ..clause_generation_helper.g_limit_clauses import g_limit_clauses

#clause utils
from ..clause_generation_helper.utils import buckets, visible_search_space, front_to_back_lb, front_to_front_lb, solution_is_below_c_star

clause_dependency={"buckets_clauses": [buckets, visible_search_space, buckets_clauses],
                   "":[]

}

def clause_generation(bound: str, bound_type: str, locality: str, problem: str, bound_constraints_path_prefix: str, path_suffix, search_path: str):
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
    required_clauses=bounds[bound]

    requires_recalculation=False  

    for clause_type in required_clauses:
        path=bound_constraints_path_prefix+clause_type+'/'+path_suffix
        if not exists(path):
            requires_recalculation=True
            break

    # WARNING IF ONE CLAUSE NEEDS RECUCLATING ALL NEED TO BE RECALCULATED AS THE CONSISTENCY OF VARIABLE NUMBERING MUST BE MAINTAINED
    if requires_recalculation:
        max_node_id, epsilon_global, iota_global, solution_nodes_f, solution_nodes_b, closed_list_f, closed_list_b = deserialize(search_path+problem+".obj")
        avaliable_variable=max_node_id

        global_info = True if locality == 'global' else False
        node_lower_bound_func = front_to_back_lb if bound_type == 'front_to_back' else front_to_front_lb
        
        # Begin clause genration

        # Dependant set 1
        buckets_f = buckets(closed_list_f, epsilon_global, iota_global, global_info)
        buckets_b = buckets(closed_list_b, epsilon_global, iota_global, global_info)
        must_expand_paired_buckets, might_expand_paired_buckets = visible_search_space (node_lower_bound_func, buckets_f, buckets_b, solution_nodes_f[0].g)

        mep = must_expand_clauses(must_expand_paired_buckets, buckets_f, buckets_b)
        serialize(mep, bound_constraints_path_prefix+'must_expand_clauses/'+path_suffix)
        mep = []

        parentage = parentage_clauses(might_expand_paired_buckets, must_expand_paired_buckets, buckets_f, buckets_b)
        serialize(parentage, bound_constraints_path_prefix+'parent_clauses/'+path_suffix)
        parentage = []        

        bucket_aliases_f, bucket_aliases_b, avaliable_variable, bucket = buckets_clauses(might_expand_paired_buckets, must_expand_paired_buckets, buckets_f, buckets_b, avaliable_variable)
        serialize(bucket, bound_constraints_path_prefix+'buckets_clauses/'+path_suffix)
        bucket = []

        avaliable_variable, gLimit = g_limit_clauses(bucket_aliases_f, bucket_aliases_b,  solution_nodes_f[0].g, epsilon_global, avaliable_variable)
        serialize(gLimit, bound_constraints_path_prefix+'g_limit_clauses/'+path_suffix)
        gLimit = []

        #is there a viasable search space clause???! DEPENDS ON HOW mep AND buckets CLAUSES ARE MADE.

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

        collision_below_c_star = solution_is_below_c_star(node_lower_bound_func, solution_nodes_f, closed_list_b, solution_nodes_f[0].g, epsilon_global, iota_global, global_info)

        return avaliable_variable, collision_below_c_star
    return None