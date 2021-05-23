def gap_unit_cost(node, goal_state):
    state=node.state
    heuristic_value=0

    for i in range(0,len(state)-1):
        goal_position_i=goal_state.index(state[i])

        j=i+1
        pancake_j=state[j]
        
        #Test if pancake j is adjacent to pancake i in the goal_state
        if goal_position_i != 0 and goal_state[goal_position_i + -1] == pancake_j:
            continue
        elif goal_position_i != len(state)-1 and goal_state[goal_position_i +1] == pancake_j:
            continue

        heuristic_value+=1
        
    return heuristic_value

def gap_arbitrary_cost(node, goal_state):
    state=node.state
    heuristic_value=0
    
    for i in range(0,len(state)-1):
        goal_position_i=goal_state.index(state[i])

        j=i+1
        pancake_j=state[j]
        pancake_i=state[i]
        
        #Test if pancake j is adjacent to pancake i in the goal_state
        if goal_position_i != 0 and goal_state[goal_position_i + -1] == pancake_j:
            continue
        elif goal_position_i != len(state)-1 and goal_state[goal_position_i +1] == pancake_j:
            continue
       
        heuristic_value+=min(pancake_i,pancake_j)

    return heuristic_value