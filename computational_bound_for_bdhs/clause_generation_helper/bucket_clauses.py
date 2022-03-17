from array import array
from itertools import chain


def bucket_alias_identity(nodes_in_bucket, alias: int):
    clauses=[]

    #forward implication
    implication=[-1*node.id for node in nodes_in_bucket]
    implication.append(alias)
    clauses.append(array("q", implication))

    #backward implication
    for node in nodes_in_bucket:
        clauses.append(array("q", [-1*alias, node.id]))

    return clauses

"""WARNING: dependance on might_expand_paired_buckets and  must_expand_paired_buckets being correctly constructed by the visible_search_space function in the utils modual."""
def buckets_clauses(might_expand_paired_buckets: list, must_expand_paired_buckets: list, buckets_f:dict, buckets_b:dict, available_variable:int):
    soft_clause=set()
    alias_clauses=[]
    bucket_not_expanded_clause=[]
    # NOTE: Used to construct glimit clauses
    bucket_aliases_f=[]
    bucket_aliases_b=[]
    
    for forward_bucket, backward_bucket in chain(might_expand_paired_buckets, must_expand_paired_buckets):
        forward_alias=available_variable
        backward_alias=available_variable+1
        
        bucket_aliases_f.append((forward_bucket,forward_alias))
        bucket_aliases_b.append((backward_bucket,backward_alias))

        bucket_not_expanded_alias=available_variable+2
        available_variable+=3
        
        for node in chain(buckets_f[forward_bucket], buckets_b[backward_bucket]):
            soft_clause.add(node.id)
        
        alias_clauses.extend(bucket_alias_identity(buckets_f[forward_bucket], forward_alias))
        alias_clauses.extend(bucket_alias_identity(buckets_b[backward_bucket], backward_alias))
        alias_clauses.append(array("q", [-1*bucket_not_expanded_alias, -1*forward_alias]))
        alias_clauses.append(array("q", [-1*bucket_not_expanded_alias, -1*backward_alias]))
        bucket_not_expanded_clause.append(bucket_not_expanded_alias)
    
    if alias_clauses:
        alias_clauses += [array("q", bucket_not_expanded_clause)]
    return bucket_aliases_f, bucket_aliases_b, available_variable, [soft_clause, alias_clauses]
