import array
from aStar.utilities.serialization import serialize, deserialize
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2

def solveSAT(softClauses, hardClauses, softClauseWeight, max_node_id, must_expand_pair_nodes):
        rc2=RC2(WCNF())
        for clause in hardClauses:
            rc2.add_clause(clause)
        
        if softClauseWeight == 1:
            for clause in softClauses:
                rc2.add_clause(array.array("q",[clause]), weight=1)
        elif softClauseWeight ==-1:
            for clause in softClauses:
                rc2.add_clause(array.array("q",[-1*clause]), weight=1)

        model=rc2.compute()
        number_of_nodes_set_to_true=0
        number_of_must_expand_nodes_set_to_true=0
        for literal in model:
            if literal>0 and literal<=max_node_id:
                number_of_nodes_set_to_true+=1
            if literal in must_expand_pair_nodes:
                number_of_must_expand_nodes_set_to_true+=1
        
        return [number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true ,model]

def sat(problem: str, bound_type: str, constraints_path: str):
    return