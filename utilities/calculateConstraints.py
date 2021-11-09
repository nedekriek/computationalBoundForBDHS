import math
import os
import sys 
sys.path.append("..")
from  computationalBoundForBDHS.utilities.serialization import serialize
from  computationalBoundForBDHS.dataStructures.node import Node

def parentConstraints(filename, closedListForward, closedListBackward):
    constraints=[]

    for node in closedListForward:
        constraint =[-1*node.id]
        for parent in node.parents:
            constraint.append(parent.id)
        constraints.append(constraint)

    for node in closedListBackward:
        constraint =[-1*node.id]
        for parent in node.parents:
            constraint.append(parent.id)
        constraints.append(constraint)

    location='parents/'+filename
    serialize(constraints, location)

def mustExpandPairConstraints(filename, closedListForward, closedListBackward,  cStar, epsilon, iota):
    constraints=[]
    constraintsCStarLevel = []

    for nodeForward in closedListForward.values():
            for nodeBackward in closedListBackward.values():
                    lowerBoundOnSolutionPath=max(nodeForward.g+nodeBackward.g+epsilon,nodeForward.f+nodeBackward.d, nodeBackward.f + nodeForward.d, iota * math.ceil(((nodeForward.b+nodeBackward.b)/2)/iota))
                    if lowerBoundOnSolutionPath < cStar:
                        constraints.append([nodeForward.id, nodeBackward.id]) 
                    elif lowerBoundOnSolutionPath == cStar:
                        constraintsCStarLevel.append([nodeForward.id, nodeBackward.id])
                        
    location='mustExpandPairs/'+filename
    serialize(constraints, location)
    location='mustExpandPairsCStarLevel/'+filename
    serialize(constraintsCStarLevel,location)


def collisionConstraints(filename, solutionNodesForward, solutionNodesBackward):
    constraintsExactlyOneCollision=[]
    constraintsNoCollision=[]

    #get paths from forward computationalBoundForBDHS search
    pathsForward=[]
    for node in solutionNodesForward:
        pathsForward += node.paths()
    #get paths from backward computationalBoundForBDHS search
    pathsBackward=[]
    for node in solutionNodesBackward:
        pathsBackward += node.paths()

    optimalPathsBackwardsNodes=dict()
    for path in pathsBackward:
        for node in path:
            optimalPathsBackwardsNodes[node.state]=node

    collisionPairs=[]
    for path in pathsForward:
        i=0
        j=2
        while j < len(path):
            partnerState=path[j].state
            node=path[i]
            partnerNode=optimalPathsBackwardsNodes[partnerState]
            collisionPairs.append(node.id, partnerNode.id)
            i+=1
            j+=1

    #exactly one collision constraint calculation
    dummyCollisionVariable=(Node.count)+1
    collisionClause=[]
    for collisionPair in collisionPairs:
        constraintsExactlyOneCollision.append([-1*dummyCollisionVariable, collisionPair[0]])
        constraintsExactlyOneCollision.append([-1*dummyCollisionVariable, collisionPair[1]])
        collisionClause.append(collisionClause)
    
    #no collision constraints calculation
    for collisionPair in collisionPairs:
        u=collisionPair[0]
        v=collisionPair[1]
        constraintsNoCollision.append([[-1*u,v]])
        constraintsNoCollision.append([[u,v*-1]])

    softCollisionConstraints = collisionClause
    
    location='oneCollision/'+filename
    serialize([constraintsExactlyOneCollision,softCollisionConstraints], location)
    location='noCollision/'+filename
    serialize(constraintsNoCollision,location)


