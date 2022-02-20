
from ctypes import sizeof
from math import fabs
from operator import truediv
from platform import node
import re


class Errors:
    output = "result.txt"

    @staticmethod    
    def undefinedState(state):
        stream = open(Errors.output, "w")
        stream.write(f"Error:\nE1: A state '{state}' is not in the set of states")
        stream.close()
        exit(0)

    @staticmethod  
    def disjointStates():
        stream = open(Errors.output, "w")
        stream.write("Error:\nE2: Some states are disjoint")
        stream.close()
        exit(0)

    @staticmethod  
    def undefinedTransion(trans):
        stream = open(Errors.output, "w")
        stream.write(f"Error:\nE3: A transition '{trans}' is not represented in the alphabet")
        stream.close()
        exit(0)

    @staticmethod  
    def undefinedUnitialState():
        stream = open(Errors.output, "w")
        stream.write("Error:\nE4: Initial state is not defined")
        stream.close()
        exit(0)

    @staticmethod  
    def malformedInput():
        stream = open(Errors.output, "w")
        stream.write("Error:\nE5: Input file is malformed")
        stream.close()
        exit(0)


class Warnings:

    output: str = "result.txt"
    
    @staticmethod
    def undefinedAcceptedState():
        stream = open(Errors.output, "a")
        stream.write("W1: Accepting state is not defined")
        stream.close()
        
    @staticmethod
    def unreachableStates():
        stream = open(Errors.output, "a")
        stream.write("W2: Some states are not reachable from the initial state")
        stream.close()

    @staticmethod
    def fsaNondeterministic():
        stream = open(Errors.output, "a")
        stream.write("W3: FSA is nondeterministic")
        stream.close()


def parse(data: list):
    if (len(data) != 5):
        Errors.malformedInput()
        
    data[0] = data[0].replace("states=","");
    data[1] = data[1].replace("alpha=", "");
    data[2] = data[2].replace("init.st=", "");
    data[3] = data[3].replace("fin.st=", "");
    data[4] = data[4].replace("trans=", "")

    for i in range(len(data)):
        data[i] = data[i].replace("[", "")
        data[i] = data[i].replace("]", "")
        data[i] = data[i].replace("\n", "")
        
        if ">" in data[i]:
            data[i] = data[i].replace(">", ",")
            
        if "," in data[i]:
            data[i] = data[i].split(",")
        else:
            if (len(data[i]) == 0):
                data[i] = []
            else:
                data[i] = [data[i]]
            
    
    return data;


def checkStates(states, inits, fins, trans):
    #checking states in trans
    for i in range(0, len(trans), 3):
        if trans[i] not in states:
            Errors.undefinedState(trans[i])
    
    #checking states in fins
    for st in fins:
        if st not in states:
            Errors.undefinedState(st)
    
    #checking states in inits
    for st in inits:
        if st not in states:
            Errors.undefinedState(st)


def checkInitState(inits):
    if (len(inits) == 0):
        Errors.undefinedUnitialState()


def checkAlphabet(trans, alphas):
    for i in range(1, len(trans), 3):
        if trans[i] not in alphas:
            Errors.undefinedTransion(trans[i])


def checkFormat(data):
    if (len(data) != 5):
        Errors.malformedInput()


def chechConnection(trans):
    nodes = []
    tree = []
    
    for i in range(0, len(trans), 3):
        nodes.append(trans[i])
        
    for i in range(1, len(nodes), 2):
        if (nodes[i] == nodes[i - 1]):
            if (len(tree) == 0):
                tree.append([nodes[i]])
                continue
                
            if not isInAnyBranch(tree, nodes[i]):
                tree.append([nodes[i]])
        
        else:
            if (len(tree) == 0):
                tree.append([nodes[i], nodes[i-1]])
                continue
        
            index1 = getIndexOfBranch(nodes[i])
            index2 = getIndexOfBranch(nodes[i - 1])
            
            if index1 != -1 and index2 != -1:
                newBranch = tree[index1] + tree[index2]
                tree.append(newBranch)
                tree.pop(index1)
                tree.pop(index2)
                continue
                
            if index1 == -1 and index2 == -1:
                tree.append([nodes[i], nodes[i-1]])
                continue
            
            if index1 == -1:
                tree[index2].append(nodes[i-1])
            else:
                tree[index2].append(nodes[i])
                
    if len(tree) != 1:
        Errors.disjointStates()
                

def isInAnyBranch(tree, node):
    for branch in tree:
        if node in branch:
            return True
    
    return False


def getIndexOfBranch(tree, node):
    for i in range(len(tree)):
        if node in tree[i]:
            return i
        
    return -1;


def validate(data: list):
    
    checkFormat(data)
    
    states = data[0]
    alphas = data[1]
    inits = data[2]
    fins = data[3]
    trans = data[4]
    
    checkStates(states, inits, fins, trans)
    
    checkInitState(inits)
    
    checkAlphabet(trans, alphas)



    

    

def main():
    stream = open("fsa.txt", "r")
    data = stream.readlines()
    stream.close()
    
    data = parse(data)
    validate(data)

main()