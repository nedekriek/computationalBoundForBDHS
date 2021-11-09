from array import array

def must_expand_clauses(must_expand_paired_buckets: list, buckets_f: dict, buckets_b: dict):
    soft_clause=set()      #node_aliases
    hard_clauses=[]        #must_expand_pairs

    for node_values_f, node_values_b in must_expand_paired_buckets:
        for node_f in buckets_f[node_values_f]:
            for node_b in buckets_b[node_values_b]:
                soft_clause.add(node_f.id)
                soft_clause.add(node_b.id)
                hard_clauses.append(array("q", [node_f.id, node_b.id]))
    
    return [soft_clause, hard_clauses]