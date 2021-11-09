import array
from itertools import chain
import sys
sys.path.append("..")

from aStar.utilities.utils import getIndex
from aStar.utilities.serialization import serialize, deserialize
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2

import csv

class Sat:
    def __init__(self, constraintsDir, resultsPath, satDir, problem_list):

        self.constraintsDir = constraintsDir
        self.resultsPath = resultsPath
        self.satDir=satDir
        self.index=getIndex(problem_list)

        self.soft_clause_weight={"experiment1":-1,
                            "experiment2":-1,
                            "experiment3":-1,
                            "experiment4":1}
        
    def _solveSAT(self, softClauses, hardClauses, softClauseWeight, max_node_id, must_expand_pair_nodes):
        rc2=RC2(WCNF())
        for clause in hardClauses:
            rc2.add_clause(clause)
        
        if softClauseWeight == 1:
            for clause in softClauses:
                rc2.add_clause(array.array("q",[clause]), weight=1)
        elif softClauseWeight ==-1:
            for clause in softClauses:
                rc2.add_clause(array.array("q",[-1*clause]), weight=1)

        model=rc2.compute()
        number_of_nodes_set_to_true=0
        number_of_must_expand_nodes_set_to_true=0
        for literal in model:
            if literal>0 and literal<=max_node_id:
                number_of_nodes_set_to_true+=1
            if literal in must_expand_pair_nodes:
                number_of_must_expand_nodes_set_to_true+=1
        
        return [number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true ,model]

    def deserialize_must_expand_pairs(self, soft_clauses, hard_clauses, constraints_deserialized, case):
        constraints_deserialized.add("must_expand_pairs")
        data = deserialize(self.constraintsDir+"/must_expand_pairs/"+case+".obj")
        soft_mep_clauses, mep_clauses = data
        soft_clauses.extend(soft_mep_clauses)
        hard_clauses.extend(mep_clauses)

    def deserialize_parents(self, soft_clauses, hard_clauses, constraints_deserialized, case):
        constraints_deserialized.add("parents")
        parent_constraints = deserialize(self.constraintsDir+"/parents/"+case+".obj")
        hard_clauses.extend(parent_constraints)

    def run(self, experiments=["experiment1","experiment2","experiment3","experiment4"]):
        headers=["case", "c_star", "collision_below_c_star", "ex1", "ex2", "ex3", "ex4","ex4_original", "MEP_ex1", "MEP_ex2", "MEP_ex3", "MEP_ex4"]
        with open(self.resultsPath, "a") as file:
                writer=csv.writer(file)
                writer.writerow(headers)
        for case in self.index:
            max_node_id, dummy_variable, c_star, collision_below_c_star = deserialize(self.constraintsDir+"/encoding_information/"+case+".obj")
            row={"case":case, "c_star":c_star, "collision_below_c_star":collision_below_c_star,
                 "ex1":None, "ex2":None, "ex3":None, "ex4":None, "MEP_ex1":None, "MEP_ex2":None, "MEP_ex3":None, "MEP_ex4":None}
            
            constraints_deserialized=set()
            soft_clauses=[]
            hard_clauses=[]
            self.deserialize_must_expand_pairs(soft_clauses, hard_clauses, constraints_deserialized, case)
            must_expand_pair_nodes=set(soft_clauses)
            
            if "experiment1" in experiments:
                number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true ,model=self._solveSAT(soft_clauses,hard_clauses, self.soft_clause_weight["experiment1"], max_node_id, must_expand_pair_nodes)
                
                row["ex1"]=number_of_nodes_set_to_true
                row["MEP_ex1"]=number_of_must_expand_nodes_set_to_true
                serialize(model, self.satDir+"/experiment1/"+case+".obj")

            if "experiment2" in experiments:
                if "must_expand_pairs" not in constraints_deserialized:
                    self.deserialize_must_expand_pairs(soft_clauses, hard_clauses, constraints_deserialized, case)
                self.deserialize_parents(soft_clauses, hard_clauses, constraints_deserialized, case)
                
                number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true ,model=self._solveSAT(soft_clauses,hard_clauses, self.soft_clause_weight["experiment2"], max_node_id, must_expand_pair_nodes)
                
                row["ex2"]=number_of_nodes_set_to_true
                row["MEP_ex2"]=number_of_must_expand_nodes_set_to_true
                serialize(model, self.satDir+"/experiment2/"+case+".obj")

            if "experiment3" in experiments:
                if "must_expand_pairs" not in constraints_deserialized:
                    self.deserialize_must_expand_pairs(soft_clauses, hard_clauses, constraints_deserialized, case)
                if "parents" not in constraints_deserialized:
                    self.deserialize_parents(soft_clauses, hard_clauses, constraints_deserialized, case)

                _, at_least_one_collision = deserialize(self.constraintsDir+"/at_least_one_collision/"+case+".obj")
                hard_clauses.extend(at_least_one_collision)
                data=deserialize(self.constraintsDir+"/nodes_bound_by_c_star/"+case+".obj")
                soft_clauses.extend(data)

                number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true ,model=self._solveSAT(soft_clauses,hard_clauses, self.soft_clause_weight["experiment3"], max_node_id, must_expand_pair_nodes)

                row["ex3"]=number_of_nodes_set_to_true
                row["MEP_ex3"]=number_of_must_expand_nodes_set_to_true
                serialize(model, self.satDir+"/experiment3/"+case+".obj")

            if "experiment4" in experiments:
                soft_clauses=[]
                hard_clauses=[]

                self.deserialize_parents(soft_clauses, hard_clauses, constraints_deserialized, case)
                _, soft_buckets, hard_buckets =deserialize(self.constraintsDir+"/buckets/"+case+".obj")
                soft_clauses.extend(soft_buckets)
                hard_clauses.extend(hard_buckets)
                data=deserialize(self.constraintsDir+"/nodes_bound_by_c_star/"+case+".obj")
                soft_clauses.extend(data)
                if not collision_below_c_star:
                    data=deserialize(self.constraintsDir+"/no_collision/"+case+".obj")

                number_of_nodes_set_to_true, number_of_must_expand_nodes_set_to_true ,model=self._solveSAT(soft_clauses,hard_clauses, self.soft_clause_weight["experiment4"], max_node_id, must_expand_pair_nodes)

                row["ex4_original"]=number_of_nodes_set_to_true
                row["ex4"]=number_of_nodes_set_to_true+1
                row["MEP_ex4"]=number_of_must_expand_nodes_set_to_true
                serialize(model, self.satDir+"/experiment4/"+case+".obj")

            with open(self.resultsPath, "a") as file:
                writer=csv.writer(file)
                line=[row[column_header] for column_header in headers]
                writer.writerow(line)


# print("unit cost")
# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# case_names=["five_pancakes", "four_pancakes", "three_pancakes", "six_pancakes", "seven_pancakes"]
# for i,file in enumerate(file_to_run_search):
#     se = Sat("experiments/constraints/constraints_only_unit_cost_pancake", "experiments/results/used_in_dissertation/unit_cost_"+case_names[i]+".csv", "experiments/satAssignments", file)
#     se.run(experiments=["experiment3","experiment4"])
#     print(file)
#     print("done")

# print("tile")
# file_to_run_search=[162,122,81,41,40]
# for i, file in enumerate(file_to_run_search):
#     se = Sat("experiments/constraints/constraints_only_unit_cost_sliding_tile", "experiments/results/used_in_dissertation/unit_cost_sliding_tile"+str(file)+".csv", "experiments/satAssignments", "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt")
#     se.run(experiments=["experiment3","experiment4"])
#     print(file)
#     print("done")


# print("arbitrary cost (global)")

# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# case_names=["five_pancakes", "four_pancakes", "three_pancakes", "six_pancakes", "seven_pancakes"]
# for i, file in enumerate(file_to_run_search):
#     se = Sat("experiments/constraints/constraints_only_arbitrary_cost_pancake", "experiments/results/used_in_dissertation/global_arbitrary_cost_"+case_names[i]+".csv", "experiments/satAssignments", file)
#     se.run()
#     print(file)
#     print("done")

# print("tile")

# file_to_run_search=[162,122,81,41,40]
# for i, file in enumerate(file_to_run_search):
#     se = Sat("experiments/constraints/constraints_only_arbitrary_cost_sliding_tile", "experiments/results/used_in_dissertation/global_arbitrary_cost_sliding_tile"+str(file)+".csv", "experiments/satAssignments", "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt")
#     se.run()
#     print(file)
#     print("done")


# print("arbitrary cost (relative)")

# file_to_run_search=['pancake/pancakeTestCases/fivePancakes.txt','pancake/pancakeTestCases/fourPancakes.txt','pancake/pancakeTestCases/threePancakes.txt','pancake/pancakeTestCases/sixPancakes.txt','pancake/pancakeTestCases/sevenPancake.txt']
# case_names=["five_pancakes", "four_pancakes", "three_pancakes", "six_pancakes", "seven_pancakes"]
# for i, file in enumerate(file_to_run_search):
#     se = Sat("experiments/constraints/constraints_only_relative_arbitrary_cost_pancake", "experiments/results/used_in_dissertation/relative_arbitrary_cost_"+case_names[i]+".csv", "experiments/satAssignments", file)
#     se.run()
#     print(file)
#     print("done")

# print("tile")

# file_to_run_search=[162,122,81,41,40]
# for i,file in enumerate(file_to_run_search):
#     se = Sat("experiments/constraints/constraints_only_arbitrary_relative_cost_sliding_tile", "experiments/results/used_in_dissertation/relative_arbitrary_cost_sliding_tile"+str(file)+".csv", "experiments/satAssignments", "slidingTile/slidingTileTestCases/8slidingTile"+str(file)+".txt")
#     se.run()
#     print(file)
#     print("done")


