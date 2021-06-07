from array import array
from itertools import chain


"""WARNING: dependance on buckets_clauses being correctly constructed by the buckets_clauses function in the buckets_clauses modual."""
def gLimit_clauses(bucket_aliases_f: list, bucket_aliases_b: list, c_star:int, global_epsilon:int, avaliable_variable:int):
    
    g_lim_aliases_f={i:avaliable_variable+1 for i in range(c_star+1)}  #by defintion a glim band is not empty so all must be included
    g_lim_aliases_b={i:avaliable_variable+1 for i in range(c_star+1)}

    avaliable_variable+=2*len(g_lim_aliases_f)

    #define g_lims
    g_lim_clauses=[]
    
    g_lims_f={key:[] for key in g_lim_aliases_f.values()}
    g_lims_b={key:[] for key in g_lim_aliases_b.values()}

    #glim_f_x only allows nodes n where g_f(n) < x to be expanded
    for bucket, alias in bucket_aliases_f:
        g_value=bucket[0]
        for i in range(c_star,g_value+1,-1):
            g_lim_f=g_lim_aliases_f[i]
            g_lims_f[g_lim_f].append(alias)
    
    #glim_b_x only allows nodes n where g_b(n) < x to be expanded
    for bucket, alias in bucket_aliases_b:
        g_value=bucket[0]
        for i in range(c_star,g_value+1,-1):
            g_lim_b=g_lim_aliases_b[i]
            g_lims_b[g_lim_b].append(alias)

    for g_lim, buckets in chain(g_lims_f, g_lims_b):
        #forward implication
        for bucket in buckets:
            g_lim_clauses.append(array("q",[-1*g_lim, -1*bucket]))
        #backward implication 
        g_lim_clauses.append(array("q",[g_lim]+buckets))

    #define g_lim behaviour
    gLSum=c_star-global_epsilon+1
    split_aliases=[]
    g_lim_split_clauses=[]

    for g_lim_f in range(gLSum+1):
        g_lim_b=gLSum-g_lim_f
        split_aliases.append(avaliable_variable)
        #forward implication
        g_lim_split_clauses.append(array("q",[-1*avaliable_variable, g_lim_f]))
        g_lim_split_clauses.append(array("q",[-1*avaliable_variable, g_lim_b]))
        #backward impication
        g_lim_split_clauses.append(array("q",[avaliable_variable, -1*g_lim_f, -1*g_lim_b]))
        avaliable_variable+=1

    xor_split_clauses=[]
    b=avaliable_variable
    avaliable_variable+=1
    #forward implication
    xor_split_clauses.append(array("q", [-1*b, split_aliases[0], split_aliases[1]]))
    xor_split_clauses.append(array("q", [-1*b, -1*split_aliases[0], -1*split_aliases[1]]))
    #backward implication
    xor_split_clauses.append(array("q", [b, -1*split_aliases[0], split_aliases[1]]))
    xor_split_clauses.append(array("q", [b, split_aliases[0], -1*split_aliases[1]]))

    for a in split_aliases[2:]:
        #forward implication
        xor_split_clauses.append(array("q", [-1*avaliable_variable, b, a]))
        xor_split_clauses.append(array("q", [-1*avaliable_variable, -1*b, -1*a]))
        #backward implication
        xor_split_clauses.append(array("q", [avaliable_variable, -1*b, a]))
        xor_split_clauses.append(array("q", [avaliable_variable, b, -1*a]))
        b=avaliable_variable
        avaliable_variable+=1

    return avaliable_variable, g_lim_clauses+g_lim_split_clauses+xor_split_clauses