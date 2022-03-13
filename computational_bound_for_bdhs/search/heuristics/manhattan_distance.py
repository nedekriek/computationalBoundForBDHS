def manhattan_distance(currentLocation, goalLocation):
    return abs(currentLocation[0]-goalLocation[0]) + abs(currentLocation[1]-goalLocation[1])

def manhattan_unit_cost(node, goalState):
    state=node.state
    h=0
    for i in range(1,len(state)): #skip the blank tile
        h+=manhattan_distance(state[i],goalState[i])
    return h

def manhattan_arbitrary_cost(node, goalState):
    state=node.state
    h=0
    for i in range(1,len(state)): #skip the blank tile
        h+=i*manhattan_distance(state[i],goalState[i])
    return h