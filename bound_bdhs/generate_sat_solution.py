import array

from pysat.formula import WCNF
from pysat.examples.rc2 import RC2

from .constants import soft_clause_weight_by_bound_type, bounds_to_clause
from .utils import serialize, deserialize


def solve_sat_problem(soft_clauses, hard_clauses, soft_clause_weight):
        rc2=RC2(WCNF())
        for clause in hard_clauses:
            rc2.add_clause(clause)
        
        if soft_clause_weight == 1:
            for clause in soft_clauses:
                rc2.add_clause(array.array("q",[clause]), weight=1)
        elif soft_clause_weight ==-1:
            for clause in soft_clauses:
                rc2.add_clause(array.array("q",[-1*clause]), weight=1)

        model=rc2.compute()

        
        return model

def sat(collision_below_c_star: bool, max_node_id: int, bound: str, bound_type :str, sat_path: str, path_suffix: str, bound_constraints_path_prefix: str):
    soft_clause_weight = soft_clause_weight_by_bound_type[bound]
    bound_clauses = bounds_to_clause[bound]
    if bound in ('ub_nx', 'ub_nx_with_g_limits'):
        if collision_below_c_star:
            bound_clauses.remove('no_collision_clauses')
        else:
            bound_clauses.remove('not_must_expand_pair_clause')

    must_expand_pair_nodes, _ =set(deserialize(bound_constraints_path_prefix+'must_expand_clauses'+path_suffix))

    soft_clauses = []
    hard_clauses = []

    for clause_set in bound_clauses:
        soft, hard = deserialize(bound_constraints_path_prefix+clause_set+path_suffix)
        if soft:
            soft_clauses.append(soft)
        if hard:
            hard_clauses.append(hard)

    sat_model = solve_sat_problem(soft_clauses, hard_clauses, soft_clause_weight)

    number_of_nodes_set_to_true=0
    number_of_must_expand_nodes_set_to_true=0
        
    for literal in sat_model:
        if literal>0 and literal<=max_node_id:
            number_of_nodes_set_to_true+=1
        if literal in must_expand_pair_nodes:            
            number_of_must_expand_nodes_set_to_true+=1

    serialize(sat_model, sat_path)    

    return number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true

        
    