from itertools import permutations

from computational_bound_for_bdhs.bound_bdhs.utils import deserialize


def run():
    examples = []
    for initial in permutations("123456", 6):
        initial = "".join(initial)
        if initial == "123456":
            continue
        problem = initial + "7_1234567"
        f2e_me_nodes, f2e_me_pairs = deserialize(f"results/Pancake_arbitrary/constraints/d0/ub/front_to_end/global/must_expand_clauses/{problem}.obj")
        f2f_me_nodes, f2f_me_pairs = deserialize(f"results/Pancake_arbitrary/constraints/d0/ub/front_to_front/global/must_expand_clauses/{problem}.obj")
        if f2e_me_nodes == f2f_me_nodes:
            continue
        examples.append(problem)
    print(examples[::-1])


if __name__ == "__main__":
    run()
