from functools import reduce
from math import ceil, gcd

def front_to_back_lb(node_values_f, node_values_b):
    g_value_f, f_value_f , d_value_f , b_value_f , epsilon_f , iota_f =  node_values_f
    g_value_b, f_value_b , d_value_b , b_value_b , epsilon_b , iota_b =  node_values_b
    
    iota=reduce(gcd, [iota_f, iota_b])
    
    return max(g_value_f + g_value_b + min(epsilon_f, epsilon_b),
               f_value_f + d_value_b, 
               f_value_b + d_value_f,
               iota * ceil(((b_value_f + b_value_b)/2)/ iota))

def front_to_front_lb(node_values_f, node_values_b):
    g_value_f, _ , _ , _ , epsilon_f , _ =  node_values_f
    g_value_b, _ , _ , _ , epsilon_b , _ =  node_values_b
    
    return g_value_f + g_value_b + min(epsilon_f, epsilon_b)

def get_node_values(node, epsilon_global: int, iota_global: int, global_info:bool):
    return (node.g, 
             node.f, 
             node.d, 
             node.b,
             node.epsilon if node.epsilon and not global_info else epsilon_global,
             node.iota if node.iota and not global_info else iota_global)

def buckets(closed_list: dict, epsilon_global: int, iota_global: int, global_info:bool):
    buckets=dict()

    for node in closed_list.values():
        key=get_node_values(node, epsilon_global, iota_global, global_info)
        if key in buckets:
            buckets[key].add(node)
        else:
            buckets[key]=set([node])
    
    return buckets 

def visible_search_space(node_lower_bound_func, buckets_f:dict, buckets_b:dict, c_star: int):
    must_expand_paired_buckets=[]
    might_expand_paired_buckets=[]
    
    for node_values_f in buckets_f.keys():
        for node_values_b in buckets_b.keys():
            lb= node_lower_bound_func(node_values_f, node_values_b) 
            if lb <= c_star:
                if lb < c_star:
                    must_expand_paired_buckets.append([node_values_f, node_values_b])
                else:
                    might_expand_paired_buckets.append([node_values_f, node_values_b])
    
    return must_expand_paired_buckets, might_expand_paired_buckets

def solution_is_below_c_star(node_lower_bound_func, solution_nodes_f: list, closed_list_b: dict, c_star:int, epsilon_global:int, iota_global:int, global_info: bool):
        #get all paths
        paths_f=[]                               
        for node in solution_nodes_f:
            paths_f += node.path_sequence()
        
        #check that there is at least one path where each pair of nodes on the path is a must expand pair
        for path in paths_f:
            path_len=len(path)
            for index_f in range(path_len):
                if index_f == path_len-1:
                    return True
                node_f=path[index_f]
                for backward_index in range(index_f+1, path_len):
                    node_b=closed_list_b[path[backward_index].state]
                    node_values_f=get_node_values(node_f, epsilon_global, iota_global, global_info)
                    node_values_b=get_node_values(node_b, epsilon_global, iota_global, global_info)
                    lb=node_lower_bound_func(node_values_f, node_values_b)
                    if lb >= c_star:
                        break ##this was incorrect as it said return false
        return False
