if clause_type == 'buckets_clauses':
            path=start_path+'/buckets_clauses'+end_path
            if not exists(path) or overwrite_flag:
                continue
        if clause_type == 'must_expand_clauses':
            path=start_path+'/must_expand_clauses'+end_path
            if not exists(path) or overwrite_flag:
                continue
        if clause_type == 'parent_clauses':
            path=start_path+'/parent_clauses'+end_path
            if not exists(path) or overwrite_flag:
                continue
        if clause_type == 'no_collision_clauses':
            path=start_path+'/no_collision_clauses'+end_path
            if not exists(path) or overwrite_flag:
                continue
        if clause_type == 'at_least_one_collision_clauses':
            path=start_path+'/at_least_one_collision_clauses'+end_path
            if not exists(path) or overwrite_flag:
                continue
        if clause_type == 'g_limit_clauses':
            path=start_path+'/g_limit_clauses'+end_path
            if not exists(path) or overwrite_flag:
                continue