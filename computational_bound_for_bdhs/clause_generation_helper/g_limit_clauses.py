from array import array
from itertools import chain


"""WARNING: dependance on buckets_clauses being correctly constructed by the buckets_clauses function in the buckets_clauses modual."""
def g_limit_clauses(bucket_aliases_f: list, bucket_aliases_b: list, c_star:int, epsilon_global:int, available_variable:int):
    
    #map g value to aliases 
    num_alias = c_star+1    # for only one direction
    g_lim_aliases_f={i:available_variable+i for i in range(num_alias)}  #by defintion a glim band is not empty so all must be included
    g_lim_aliases_b={i:available_variable+num_alias+i for i in range(num_alias)}

    available_variable+=2*num_alias+1 #set the newest available variable 

    #define g_lims
    g_lim_clauses=[]
    
    #dictionary mapping glimits to the buckets that they DO NOT expand
    g_lims_f_by_alias={i:[] for i in g_lim_aliases_f.values()}
    g_lims_b_by_alias={i:[] for i in g_lim_aliases_b.values()}

    #glim_f_x only allows nodes n where g_f(n) < x to be expanded
    for bucket, alias in bucket_aliases_f:
        g_value=bucket[0]
        for i in range(c_star,g_value-1,-1):
            g_lim_f=g_lim_aliases_f[i]
            g_lims_f_by_alias[g_lim_f].append(alias)
    
    #glim_b_x only allows nodes n where g_b(n) < x to be expanded
    for bucket, alias in bucket_aliases_b:
        g_value=bucket[0]
        for i in range(c_star,g_value-1,-1):
            g_lim_b=g_lim_aliases_b[i]
            g_lims_b_by_alias[g_lim_b].append(alias)

    for g_lim, buckets in chain(g_lims_f_by_alias.items(), g_lims_b_by_alias.items()):
        #forward implication (glim to buckets)
        for bucket in buckets:
            g_lim_clauses.append(array("q",[-1*g_lim, -1*bucket]))
        #backward implication 
        g_lim_clauses.append(array("q",[g_lim]+buckets))

    #define g_lim behaviour
    gLSum=c_star-epsilon_global+1
    split_aliases=[]
    g_lim_split_clauses=[]

    for g_lim_f in range(gLSum+1):
        g_lim_b=gLSum-g_lim_f
        
        g_lim_f=g_lim_aliases_f[g_lim_f]
        g_lim_b=g_lim_aliases_b[g_lim_b]
        split_aliases.append(available_variable)
        
        #forward implication
        g_lim_split_clauses.append(array("q",[-1*available_variable, g_lim_f]))
        g_lim_split_clauses.append(array("q",[-1*available_variable, g_lim_b]))
        #backward impication
        g_lim_split_clauses.append(array("q",[available_variable, -1*g_lim_f, -1*g_lim_b]))
        available_variable+=1

    xor_split_clauses=[]
    b=available_variable
    available_variable+=1
    #forward implication
    xor_split_clauses.append(array("q", [-1*b, split_aliases[0], split_aliases[1]]))
    xor_split_clauses.append(array("q", [-1*b, -1*split_aliases[0], -1*split_aliases[1]]))
    #backward implication
    xor_split_clauses.append(array("q", [b, -1*split_aliases[0], split_aliases[1]]))
    xor_split_clauses.append(array("q", [b, split_aliases[0], -1*split_aliases[1]]))

    for a in split_aliases[2:]:
        #forward implication
        xor_split_clauses.append(array("q", [-1*available_variable, b, a]))
        xor_split_clauses.append(array("q", [-1*available_variable, -1*b, -1*a]))
        #backward implication
        xor_split_clauses.append(array("q", [available_variable, -1*b, a]))
        xor_split_clauses.append(array("q", [available_variable, b, -1*a]))
        b=available_variable
        available_variable+=1

    return available_variable, [None, g_lim_clauses+g_lim_split_clauses+xor_split_clauses]