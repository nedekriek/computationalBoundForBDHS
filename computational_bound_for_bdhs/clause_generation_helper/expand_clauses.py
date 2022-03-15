from array import array

def expand_clauses(lb, heuristic_function, must_expand_paired_buckets: list, might_expand_paired_buckets: list, buckets_f: dict, buckets_b: dict, bound_type: str,c_star, epsilon_global: int, iota_global: int, global_info: int, available_variable: int):
    must_expand_soft_clause=set()      #node_aliases
    must_expand_hard_clauses=[]        #must_expand_pairs 
    
    might_expand_soft_clause=set()
    
    not_must_expand_pair_aliases = []
    not_must_expand_pair_clause = []
    
    for node_values_f, node_values_b in must_expand_paired_buckets:
        for node_f in buckets_f[node_values_f]:
            for node_b in buckets_b[node_values_b]:
                n_f=node_f.id
                n_b=node_b.id

                if bound_type == 'front_to_end' or lb(node_f, node_b, heuristic_function, epsilon_global, iota_global, global_info) < c_star:
                    must_expand_soft_clause.add(n_f)
                    must_expand_soft_clause.add(n_b)
                    must_expand_hard_clauses.append(array("q", [n_f, n_b]))

                    not_must_expand_pair_aliases.append(array("q", [available_variable, -1*n_b]))       #could make into a function
                    not_must_expand_pair_aliases.append(array("q", [available_variable, -1*n_f]))
                    not_must_expand_pair_aliases.append(array("q", [-1*available_variable, n_f,n_b]))
                    not_must_expand_pair_clause.append(-1*available_variable)
                    available_variable+=1
                    
                elif lb(node_f, node_b, heuristic_function, epsilon_global, iota_global, global_info) == c_star:
                    might_expand_soft_clause.add(node_f.id)
                    might_expand_soft_clause.add(node_b.id)

                    # not_expand_pair_aliases.append(array("q", [available_variable, -1*n_b])) # should not be needed if our soft clauses includes all nodes in might expand and must expand pairs
                    # not_expand_pair_aliases.append(array("q", [available_variable, -1*n_f]))
                    # not_expand_pair_aliases.append(array("q", [-1*available_variable, n_f,n_b]))

    for node_values_f, node_values_b in might_expand_paired_buckets:
        for node_f in buckets_f[node_values_f]:
            for node_b in buckets_b[node_values_b]:
                if bound_type == 'front_to_end' or lb(node_f, node_b, heuristic_function, epsilon_global, iota_global, global_info) == c_star:
                    might_expand_soft_clause.add(node_f.id)
                    might_expand_soft_clause.add(node_b.id)

                    # not_expand_pair_aliases.append(array("q", [available_variable, -1*n_b])) # see above
                    # not_expand_pair_aliases.append(array("q", [available_variable, -1*n_f]))
                    # not_expand_pair_aliases.append(array("q", [-1*available_variable, n_f,n_b]))
    
    #might expand set minus must expand
    might_expand_soft_clause -= must_expand_soft_clause

    if not_must_expand_pair_aliases:
        not_must_expand_pair_aliases += [array("q", not_must_expand_pair_clause)]
    
    return [must_expand_soft_clause, must_expand_hard_clauses], [might_expand_soft_clause, None], [None,not_must_expand_pair_aliases]
