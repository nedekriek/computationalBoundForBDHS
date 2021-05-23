
from fractions import gcd
from functools import reduce

def getIndex(problem_list):
    """helper function reading in cases by giving case names in the form initial_goal"""
    index = []
    with open(problem_list) as cases:
            for case in cases:
                case=case.split()
                initialState = case[0].strip()
                goalState = case[1].strip()
                caseName=initialState+"_"+goalState
                index.append(caseName)
    return index


