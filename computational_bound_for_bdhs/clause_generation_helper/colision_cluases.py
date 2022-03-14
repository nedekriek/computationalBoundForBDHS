from array import array
from itertools import chain

def get_collision_locations(solution_nodes_f: list, solution_nodes_b:list, closed_list_b: dict):
    common_child_collisions=set()

    paths_f=[]                                
    for node in solution_nodes_f:
        paths_f += node.path_sequence()
    
    paths_b=[]
    for node in solution_nodes_b:
        paths_b += node.path_sequence()

    nodes_adjacent_to_terminal=set()
    for path in chain(paths_f,paths_b):
        node=path[len(path)-2]
        nodes_adjacent_to_terminal.add(node.id)

    for path in paths_f:
        i=0
        j=2
        while j< len(path):
            common_child_collisions.add((path[i].id, closed_list_b[path[j].state].id))
            i+=1
            j+=1

    common_child_collisions = [array("q", item) for item in list(common_child_collisions)]
    return [common_child_collisions, list(nodes_adjacent_to_terminal)]

def no_collision_clauses(common_child_collisions: list, nodes_adjacent_to_terminal: list):
    no_collision_clauses=[]
    for pair in common_child_collisions:
        no_collision_clauses.append(array("q",[-1*node for node in pair]))
    for node in nodes_adjacent_to_terminal:
        no_collision_clauses.append(array("q",[-1*node]))
    return [None, no_collision_clauses]

def at_least_one_collision_clauses(common_child_collisions: list, nodes_adjacent_to_terminal:list , available_variable:int):
    possible_collisions=[]
    at_least_one_collision_clauses=[]
    
    for pair in common_child_collisions:
        possible_collisions.append(available_variable)
        #c->(a ^ b) where (a,b) is a collision pair
        at_least_one_collision_clauses.append(array("q",[-1*available_variable, pair[0]]))
        at_least_one_collision_clauses.append(array("q",[-1*available_variable, pair[1]]))
        available_variable+=1

    possible_collisions.extend(nodes_adjacent_to_terminal)
    at_least_one_collision_clauses.append(array("q",possible_collisions))
    return available_variable , [None, at_least_one_collision_clauses]

