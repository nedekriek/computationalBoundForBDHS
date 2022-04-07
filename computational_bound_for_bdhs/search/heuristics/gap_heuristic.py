def gap_unit_cost_helper(state_1, state_2, *, degradation):
    # * before degradation in parameters means we must pass degradation as a kewword argument
    # This is here to avoid errors (i.e. if we forget to set degradation)
    # In practice it shouldn't make usage any different, since we have aliased the heuristic using functools in main.py
    
    heuristic_value=0

    for i in range(0,len(state_1)-1):
        j=i+1
        pancake_j=state_1[j]
        pancake_i=state_1[i]

        goal_position_i=state_2.index(pancake_i)  #goal postion is the index of the pancake in the goal state

        # Skip all pancakes with value at most degradation value 
        # e.g. for degradation=2, skip gaps involving pancakes 1 or 2
        if any([pancake_i <= degradation, pancake_j <= degradation]):
            continue

        #Test if pancake j is adjacent to pancake i in the state_2
        if goal_position_i != 0 and state_2[goal_position_i + -1] == pancake_j:
            continue
        elif goal_position_i != len(state_1)-1 and state_2[goal_position_i +1] == pancake_j:
            continue

        heuristic_value+=1
        
    return heuristic_value

def gap_arbitrary_cost_helper(state_1, state_2, *, degradation):
    # * before degradation in parameters means we must pass degradation as a kewword argument
    # This is here to avoid errors (i.e. if we forget to set degradation)
    # In practice it shouldn't make usage any different, since we have aliased the heuristic using functools in main.py
    
    heuristic_value=0
    for i in range(0,len(state_1)-1):
        j=i+1
        pancake_j=state_1[j]
        pancake_i=state_1[i]

        goal_position_i=state_2.index(pancake_i)  #goal postion is the index of the pancake in the goal state

        # Skip all pancakes with value at most degradation value 
        # e.g. for degradation=2, skip gaps involving pancakes 1 or 2
        if any([pancake_i <= degradation, pancake_j <= degradation]):
            continue
        
        #Test if pancake j is adjacent to pancake i in the state_2
        if goal_position_i != 0 and state_2[goal_position_i + -1] == pancake_j:
            continue
        elif goal_position_i != len(state_1)-1 and state_2[goal_position_i +1] == pancake_j:
            continue
       
        heuristic_value+=min(pancake_i,pancake_j)

    return heuristic_value


def gap_unit_cost(node, state_2, *, degradation):
    if type(state_2) is not tuple:
        state_2 = state_2.state
    state_1 = node.state
    return max(
        gap_unit_cost_helper(state_1, state_2, degradation=degradation),
        gap_unit_cost_helper(state_2, state_1, degradation=degradation)
    )


def gap_arbitrary_cost(node, state_2, *, degradation):
    # * before degradation in parameters means we must pass degradation as a kewword argument
    # This is here to avoid errors (i.e. if we forget to set degradation)
    # In practice it shouldn't make usage any different, since we have aliased the heuristic using functools in main.py
    if type(state_2) is not tuple:
        state_2=state_2.state
    state_1=node.state
    return max(
        gap_arbitrary_cost_helper(state_1, state_2, degradation=degradation),
        gap_arbitrary_cost_helper(state_2, state_1, degradation=degradation)
    )