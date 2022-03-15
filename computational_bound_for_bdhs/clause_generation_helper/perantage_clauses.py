
from array import array
from itertools import chain

def parentage_clauses(must_expand_paired_buckets: list, might_expand_paired_buckets:list, buckets_f: list, buckets_b:list ):
    parent_clauses=[]
    done_f=set()
    done_b=set()
    for node_values_f, node_values_b in chain(must_expand_paired_buckets, might_expand_paired_buckets):
        if node_values_f not in done_f:
            for node in buckets_f[node_values_f]:
                if node not in done_f:
                    if node.parents:
                        constraint=array("q", [-1*node.id])
                        for parent in node.parents:
                            constraint.append(parent.id)
                        parent_clauses.append(constraint)
                        done_f.add(node)
            done_f.add(node_values_f)
        if node_values_b not in done_b:
            for node in buckets_b[node_values_b]:
                if node not in done_b:
                    if node.parents:
                        constraint=array("q", [-1*node.id])
                        for parent in node.parents:
                            constraint.append(parent.id)
                        parent_clauses.append(constraint)
                        done_b.add(node)
            done_b.add(node_values_b)

    return [None, parent_clauses]