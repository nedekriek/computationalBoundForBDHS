import sys
sys.path.append("..")

from aStar.utilities.utils import getIndex
from aStar.utilities.serialization import serialize, deserialize

import array
from itertools import chain
from math import ceil, gcd


class Constraints:
    def __init__(self,searchDir, constraintsDir, problem_list):
        self.searchDir=searchDir
        self.constraintsDir = constraintsDir
        self.index=getIndex(problem_list)

        self.experiments_to_constraints={'experiment1':['must_expand_pairs'],
                                    'experiment2':['must_expand_pairs', 'parents'],
                                    'experiment3':['must_expand_pairs', 'parents', 
                                                   'at_least_one_collision','nodes_bound_by_c_star'],
                                    'experiment4':['buckets', 'parents', 
                                                   'no_collision', 'nodes_bound_by_c_star']}
        self.soft_clause_weight={'experiment1':-1,
                            'experiment2':-1,
                            'experiment3':-1,
                            'experiment4':1}
    
    def make_buckets(self, closed_list, global_epsilon, global_iota, global_information):
        buckets=dict()
        if global_information:
            for node in closed_list.values():
                key=(node.g, node.f, node.d, node.b, global_epsilon, global_iota)
                if key in buckets:
                    buckets[key].add(node)
                else:
                    buckets[key]=set([node])
        else:
            for node in closed_list.values():
                key=(node.g, node.f, node.d, node.b, node.epsilon if node.epsilon else global_epsilon, node.iota if node.iota else global_iota)
                if key in buckets:
                    buckets[key].add(node)
                else:
                    buckets[key]=set([node])
        return buckets

    def lower_bound_buckets(self, forward_bucket, backward_bucket):
        g_value_f, f_value_f , d_value_f , b_value_f , epsilon_f , iota_f =  forward_bucket
        g_value_b, f_value_b , d_value_b , b_value_b , epsilon_b , iota_b =  backward_bucket
        if not forward_bucket[-1]==backward_bucket[-1] or not forward_bucket[-2]==backward_bucket[-2]:
            epsilon_f = min(epsilon_f, epsilon_b)
            iota_f = gcd(iota_f, iota_b)
        return max(g_value_f+g_value_b+epsilon_f, f_value_f+d_value_b, f_value_b + d_value_f, iota_f * ceil(((b_value_f + b_value_b)/2)/iota_f))
    
    def lower_bound_nodes(self, node_forward, node_backward, epsilon, iota):
        return max(node_forward.g+node_backward.g+epsilon, node_forward.f+node_backward.d, node_backward.f + node_forward.d, iota * ceil(((node_forward.b+node_backward.b)/2)/iota))

    def must_expand_buckets(self, buckets_forward, buckets_backward, c_star):
        must_expand_buckets_at_c_star=[]
        must_expand_buckets_below_c_star=[]
        for forward_bucket in buckets_forward.keys():
            for backward_bucket in buckets_backward.keys():
                lower_bound=self.lower_bound_buckets(forward_bucket, backward_bucket)
                if lower_bound < c_star:
                    must_expand_buckets_below_c_star.append((forward_bucket, backward_bucket))
                elif lower_bound == c_star:
                    must_expand_buckets_at_c_star.append((forward_bucket, backward_bucket))
        return [must_expand_buckets_at_c_star, must_expand_buckets_below_c_star]

    def must_expand_pairs(self, must_expand_buckets_below_c_star, buckets_forward, buckets_backward):
        soft_clause=set()
        mep_clauses=[]

        for forward_bucket, backward_bucket in must_expand_buckets_below_c_star:
            for forward_node in buckets_forward[forward_bucket]:
                for backward_node in buckets_backward[backward_bucket]:
                    soft_clause.add(forward_node.id)
                    soft_clause.add(backward_node.id)
                    mep_clauses.append(array.array("q", [forward_node.id, backward_node.id]))
        return [soft_clause, mep_clauses]

    def bucket_ailias(self, nodes_in_bucket, ailias):
        clauses=[]

        implication=[-1*node.id for node in nodes_in_bucket]
        implication.append(ailias)
        clauses.append(array.array("q", implication))
        for node in nodes_in_bucket:
            clauses.append(array.array("q", [-1*ailias, node.id]))

        return clauses

    def buckets(self, must_expand_buckets_at_c_star, must_expand_buckets_below_c_star, buckets_forward, buckets_backward, dummy_variable):
        soft_clause=set()
        ailias_clauses=[]
        bucket_not_expanded_clause=[]
    
        for forward_bucket, backward_bucket in chain(must_expand_buckets_at_c_star, must_expand_buckets_below_c_star):
            forward_ailias=dummy_variable
            backward_ailias=dummy_variable+1
            bucket_not_expanded_ailias=dummy_variable+2
            dummy_variable+=3
            
            for node in chain(buckets_forward[forward_bucket], buckets_backward[backward_bucket]):
                soft_clause.add(node.id)
            
            ailias_clauses.extend(self.bucket_ailias(buckets_forward[forward_bucket], forward_ailias))
            ailias_clauses.extend(self.bucket_ailias(buckets_backward[backward_bucket], backward_ailias))
            ailias_clauses.append(array.array("q", [-1*bucket_not_expanded_ailias, -1*forward_ailias]))
            ailias_clauses.append(array.array("q", [-1*bucket_not_expanded_ailias, -1*backward_ailias]))
            bucket_not_expanded_clause.append(bucket_not_expanded_ailias)

        return [dummy_variable, soft_clause, ailias_clauses + [array.array("q", bucket_not_expanded_clause)]]
    
    def parents(self,buckets_forward, buckets_backward):
        parent_constraints=[]

        for bucket in chain(buckets_forward.values(), buckets_backward.values()):
            for node in bucket:
                if node.parents:
                    constraint=array.array("q", [-1*node.id])
                    for parent in node.parents:
                        constraint.append(parent.id)
                    parent_constraints.append(constraint)
        
        return parent_constraints

    def get_collision_locations(self, solutionNodesForward, solutionNodesBackward, closedListBackward):
        collisions=set()

        pathsForward=[]                                
        for node in solutionNodesForward:
            pathsForward += node.path_sequence()
        
        pathsBackward=[]
        for node in solutionNodesBackward:
            pathsBackward += node.path_sequence()

        nodes_adjacent_to_terminal=set()
        for path in chain(pathsForward,pathsBackward):
            node=path[len(path)-2]
            nodes_adjacent_to_terminal.add(node.id)

        for path in pathsForward:
            i=0
            j=2
            while j< len(path):
                collisions.add((path[i].id, closedListBackward[path[j].state].id))
                i+=1
                j+=1

        collisions = [array.array("q", item) for item in list(collisions)]
        return [collisions,list(nodes_adjacent_to_terminal)]

    def no_collision(self, collisions, nodes_adjacent_to_terminal):
        no_collision=[]
        for pair in collisions:
            no_collision.append(array.array("q",[-1*node for node in pair]))
        for node in nodes_adjacent_to_terminal:
            no_collision.append(array.array("q",[-1*node]))
        return no_collision
    
    def at_least_one_collision(self, collisions, nodes_adjacent_to_terminal, dummy_variable):
        dummy_Collision_Clause=[]
        at_least_one_collision=[]
        
        for pair in collisions:
            dummy_Collision_Clause.append(dummy_variable)
            at_least_one_collision.append(array.array("q",[-1*dummy_variable, pair[0]]))
            at_least_one_collision.append(array.array("q",[-1*dummy_variable, pair[1]]))
            dummy_variable+=1

        self.none_node_variables=frozenset(dummy_Collision_Clause)
        dummy_Collision_Clause.extend(nodes_adjacent_to_terminal)
        at_least_one_collision.append(array.array("q",dummy_Collision_Clause))
        return [dummy_variable , at_least_one_collision]
    
    def solutionMustBeFoundBelowCStarLevel(self, solutionNodesForward, closedListBackward, c_star, epsilon, iota, global_information):
        pathsForward=[]                                
        for node in solutionNodesForward:
            pathsForward += node.path_sequence()

        for path in pathsForward:
            path_len=len(path)
            for forward_index in range(path_len):
                forward_node=path[forward_index]
                if forward_index == len(path)-1:
                    break
                for backward_index in range(forward_index+1, path_len):
                    backward_node=closedListBackward[path[backward_index].state]
                    if not global_information:
                        epsilon=min(forward_node.epsilon,backward_node.epsilon)
                        iota=gcd(forward_node.iota, backward_node.iota)
                    lower_bound=self.lower_bound_nodes(forward_node, backward_node, epsilon, iota)
                    if lower_bound >= c_star:
                        return False
            return True

    def run(self,  experiments=['experiment1','experiment2','experiment3','experiment4'], global_information = True): 
  
        for case in self.index:
            constraints_to_create=set()
            for experiment in experiments:
                constraints_to_create.update(self.experiments_to_constraints[experiment])

            maxNodeId, global_epsilon, global_iota, solutionNodesForward, solutionNodesBackward, closedListForward, closedListBackward = deserialize(self.searchDir+case+".obj")
            c_star=solutionNodesForward[0].g
            dummy_variable=maxNodeId+1
            collision_below_c_star=False
            
            buckets_forward=self.make_buckets(closedListForward, global_epsilon, global_iota, global_information)
            buckets_backward=self.make_buckets(closedListBackward, global_epsilon, global_iota, global_information)
            must_expand_buckets_at_c_star, must_expand_buckets_below_c_star = self.must_expand_buckets(buckets_forward, buckets_backward, c_star)
            
            if "must_expand_pairs" in constraints_to_create:
                data=self.must_expand_pairs(must_expand_buckets_below_c_star, buckets_forward, buckets_backward)
                serialize(data, self.constraintsDir+"/must_expand_pairs/"+case+".obj")
                data=None
            
            if "experiment4" in experiments and self.solutionMustBeFoundBelowCStarLevel(solutionNodesForward, closedListBackward, c_star, global_epsilon, global_iota, global_information):
                collision_below_c_star=True
                below_c_star_forward=set()
                below_c_star_backward=set()
                for bucket_forward, bucket_backward in must_expand_buckets_below_c_star:
                    below_c_star_forward.add(bucket_forward)
                    below_c_star_backward.add(bucket_backward)
                
                for bucket_forward, bucket_backward in must_expand_buckets_at_c_star:
                    if bucket_forward in buckets_forward and not bucket_forward in below_c_star_forward:
                        del buckets_forward[bucket_forward] # a bucket maybe listed twice
                    if bucket_backward in buckets_backward and not bucket_backward in below_c_star_backward :
                        del buckets_backward[bucket_backward]

                must_expand_buckets_at_c_star=[]
                constraints_to_create.remove("no_collision")  # experiment 4 b

            if "buckets" in constraints_to_create:
                data=self.buckets(must_expand_buckets_at_c_star, must_expand_buckets_below_c_star, buckets_forward, buckets_backward, dummy_variable)
                dummy_variable, _, _ = data 
                serialize(data, self.constraintsDir+"/buckets/"+case+".obj")

            if 'nodes_bound_by_c_star' in constraints_to_create:
                data=set()
                for bucket_forward, bucket_backward in chain(must_expand_buckets_at_c_star, must_expand_buckets_below_c_star):
                    data.union(buckets_forward[bucket_forward])
                    data.union(buckets_backward[bucket_backward])

                data=list(data)
                serialize(data, self.constraintsDir+"/nodes_bound_by_c_star/"+case+".obj")
                data, must_expand_buckets_at_c_star, must_expand_buckets_below_c_star=None, None, None
            
            if "parents" in constraints_to_create:
                data = self.parents(buckets_forward, buckets_backward)
                serialize(data, self.constraintsDir+"/parents/"+case+".obj")
                data, buckets_forward, buckets_backward=None, None, None

            if "at_least_one_collision" in constraints_to_create or "no_collision" in constraints_to_create:
                collisions, nodes_adjacent_to_terminal=self.get_collision_locations(solutionNodesForward, solutionNodesBackward, closedListBackward) 
                
                if "at_least_one_collision" in constraints_to_create:
                    data=self.at_least_one_collision(collisions, nodes_adjacent_to_terminal, dummy_variable)
                    serialize(data, self.constraintsDir+"/at_least_one_collision/"+case+".obj")
                    data=None

                if "no_collision" in constraints_to_create:
                    data=self.no_collision(collisions, nodes_adjacent_to_terminal)
                    serialize(data, self.constraintsDir+"/no_collision/"+case+".obj")
                    data=None

                collisions, nodes_adjacent_to_terminal = None, None   

            data = [maxNodeId, dummy_variable, c_star, collision_below_c_star]
            serialize(data, self.constraintsDir+"/encoding_information/"+case+".obj")
# print("unit cost")

# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# for file in file_to_run_search:
#     se = Constraints("experiments/searchResults/problemPancakeUnitCost/gapUnitCost/", "experiments/constraints/constraints_only_unit_cost_pancake", file)
#     se.run(experiments=['experiment3', "experiment4"])
#     print(file)
#     print("done")

# print("tile")
# file_to_run_search=[40,41,81,122,162]
# for file in file_to_run_search:
#     se = Constraints("experiments/searchResults/problemEightPuzzleUnitCost/manhattanUnitCost/", "experiments/constraints/constraints_only_unit_cost_sliding_tile", "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt")
#     se.run(experiments=['experiment3', "experiment4"])
#     print(file)
#     print("done")

# print("arbitrary cost (global)")

# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# for file in file_to_run_search:
#     se = Constraints("experiments/searchResults/problemPancakeArbitraryCost/gapArbitraryCost/", "experiments/constraints/constraints_only_global_arbitrary_cost_pancake", file)
#     se.run(experiments=['experiment3', "experiment4"])
#     print(file)
#     print("done")

# print("tile")

# file_to_run_search=[40,41,81,122,162]
# for file in file_to_run_search:
#     se = Constraints("experiments/searchResults/problemEightPuzzleArbitraryCost/manhattanArbitraryCost/", "experiments/constraints/constraints_only_global_arbitrary_cost_sliding_tile", "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt")
#     se.run(experiments=['experiment3', "experiment4"])
#     print(file)
#     print("done")

# print("arbitrary cost (relative)")

# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# for file in file_to_run_search:
#     se = Constraints("experiments/searchResults/problemPancakeArbitraryCost/gapArbitraryCost/", "experiments/constraints/constraints_only_relative_arbitrary_cost_pancake", file)
#     se.run(global_information=False)
#     print(file)
#     print("done")

# print("tile")

# file_to_run_search=[40,41,81,122,162]
# for file in file_to_run_search:
#     se = Constraints("experiments/searchResults/problemEightPuzzleArbitraryCost/manhattanArbitraryCost/", "experiments/constraints/constraints_only_relative_arbitrary_cost_sliding_tile", "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt")
#     se.run(global_information=False)
#     print(file)
#     print("done")

