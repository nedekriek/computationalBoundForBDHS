from computational_bound_for_bdhs.bound_bdhs.utils import deserialize


def print_search_graph(problem, degradation, cost_type):
    search = deserialize(f"results/Pancake_{cost_type}/search/d{degradation}/{problem}.obj")
    print("Format: (Node ID, state, g-value, h-value, d-value, b-value)")
    print("Forward Nodes:")
    print([(node.id, node.state, node.g, node.h, node.d, node.b) for node in search[5].values()])
    print()
    print("Backward Nodes:")
    print([(node.id, node.state, node.g, node.h, node.d, node.b) for node in search[6].values()])
    print()


def print_clauses(fp):
    print(deserialize(fp))


if __name__ == "__main__":
    state = "1234576_1234567"
    print("state:",state)
    degradation = 5
    print("degradation:",degradation)
    cost_type = "unit"
    print("cost_type:",cost_type)
    search_type = "front_to_end"
    print("search_type:",search_type)
    bound_type = "ub"
    print("bound_type:",bound_type)
    print_search_graph(state, degradation, cost_type)
    print("Sat Solution")
    print(deserialize(f"results/Pancake_{cost_type}/sat/d{degradation}/{bound_type}/{search_type}/global/{state}.obj"))
    print("Must expand clauses:")
    print_clauses(f"results/Pancake_{cost_type}/constraints/d{degradation}/{bound_type}/{search_type}/global/must_expand_clauses/{state}.obj")
    print("Might expand clauses:")
    print_clauses(f"results/Pancake_{cost_type}/constraints/d{degradation}/{bound_type}/{search_type}/global/might_expand_clauses/{state}.obj")
    print("Parentage clauses:")
    print_clauses(f"results/Pancake_{cost_type}/constraints/d{degradation}/{bound_type}/{search_type}/global/parent_clauses/{state}.obj")
    print("At least one collision clauses:")
    print_clauses(f"results/Pancake_{cost_type}/constraints/d{degradation}/{bound_type}/{search_type}/global/at_least_one_collision_clauses/{state}.obj")
    print("No collision clauses:")
    print_clauses(f"results/Pancake_{cost_type}/constraints/d{degradation}/{bound_type}/{search_type}/global/no_collision_clauses/{state}.obj")
    print("Not must expand pair clauses:")
    print_clauses(f"results/Pancake_{cost_type}/constraints/d{degradation}/{bound_type}/{search_type}/global/not_must_expand_pair_clause/{state}.obj")

