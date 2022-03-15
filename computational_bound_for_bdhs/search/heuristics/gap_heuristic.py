def gap_unit_cost(node, goal_state, *, degradation):
    # * before degradation in parameters means we must pass degradation as a kewword argument
    # This is here to avoid errors (i.e. if we forget to set degradation)
    # In practice it shouldn't make usage any different, since we have aliased the heuristic using functools in main.py
    if type(goal_state) is not tuple:
        goal_state=goal_state.state

    state=node.state
    heuristic_value=0

    for i in range(0,len(state)-1):
        goal_position_i=goal_state.index(state[i])

        j=i+1
        pancake_j=state[j]
        
        # Skip all pancakes with value at most degradation value 
        # e.g. for degradation=2, skip gaps involving pancakes 1 or 2
        if any([pancake_j <= degradation, goal_position_i <= degradation]):
            continue
        #Test if pancake j is adjacent to pancake i in the goal_state
        if goal_position_i != 0 and goal_state[goal_position_i + -1] == pancake_j:
            continue
        elif goal_position_i != len(state)-1 and goal_state[goal_position_i +1] == pancake_j:
            continue

        heuristic_value+=1
        
    return heuristic_value

def gap_arbitrary_cost_helper(state_1, state_2, *, degradation):
    # * before degradation in parameters means we must pass degradation as a kewword argument
    # This is here to avoid errors (i.e. if we forget to set degradation)
    # In practice it shouldn't make usage any different, since we have aliased the heuristic using functools in main.py
    heuristic_value=0
    for i in range(0,len(state_1)-1):
        goal_position_i=state_2.index(state_1[i])

        j=i+1
        pancake_j=state_1[j]
        pancake_i=state_1[i]
        
        # Skip all pancakes with value at most degradation value 
        # e.g. for degradation=2, skip gaps involving pancakes 1 or 2
        if any([pancake_i <= degradation, pancake_j <= degradation]):
            continue
        #Test if pancake j is adjacent to pancake i in the goal_state
        if goal_position_i != 0 and state_2[goal_position_i + -1] == pancake_j:
            continue
        elif goal_position_i != len(state_1)-1 and state_2[goal_position_i +1] == pancake_j:
            continue
       
        heuristic_value+=min(pancake_i,pancake_j)

    return heuristic_value


def gap_arbitrary_cost(node, goal_state, *, degradation):
    # * before degradation in parameters means we must pass degradation as a kewword argument
    # This is here to avoid errors (i.e. if we forget to set degradation)
    # In practice it shouldn't make usage any different, since we have aliased the heuristic using functools in main.py
    if type(goal_state) is not tuple:
        goal_state=goal_state.state
    state=node.state
    return max(
        gap_arbitrary_cost_helper(state, goal_state, degradation=degradation),
        gap_arbitrary_cost_helper(goal_state, state, degradation=degradation)
    )