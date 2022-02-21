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
    isOneWar = False;
    
    @staticmethod
    def oneWarMess():
        stream = open(Errors.output, "a")
        stream.write("\nWarning:")
        stream.close()
        Warnings.isOneWar = True
    
    @staticmethod
    def undefinedAcceptedState():
        if not Warnings.isOneWar:
            Warnings.oneWarMess()
        stream = open(Errors.output, "a")
        stream.write("\nW1: Accepting state is not defined")
        stream.close()
        
    @staticmethod
    def unreachableStates():
        if not Warnings.isOneWar:
            Warnings.oneWarMess()
        stream = open(Errors.output, "a")
        stream.write("\nW2: Some states are not reachable from the initial state")
        stream.close()

    @staticmethod
    def fsaNondeterministic():
        if not Warnings.isOneWar:
            Warnings.oneWarMess()
        stream = open(Errors.output, "a")
        stream.write("\nW3: FSA is nondeterministic")
        stream.close()


def parse(data: list):
    checkFormat(data)
        
    data[0] = data[0].replace("states=","");
    data[1] = data[1].replace("alpha=", "");
    data[2] = data[2].replace("init.st=", "");
    data[3] = data[3].replace("fin.st=", "");
    data[4] = data[4].replace("trans=", "")

    for i in range(len(data)):
        data[i] = data[i].replace("[", "")
        data[i] = data[i].replace("]", "")
        data[i] = data[i].replace("\n", "")
        data[i] = data[i].replace(" ", "")
        
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
    row = ""
    for line in data:
        row+=line
    
    row = row.replace(" ", "")
    
    pattern = re.compile('states=\[([a-z0-9],?)*\]\nalpha=\[([a-z0-9_],?)*\]\ninit.st=\[.*\]\nfin.st=\[.*\]\ntrans=\[.*\]')
    result = pattern.findall(row)
    
    if (len(result) == 0):
        Errors.malformedInput()


def checkReachability(inits,trans):
    nodes = []
    tree = []
    
    tree.append(inits)
    
    for i in range(len(trans)):
        if i % 3 != 1:
            nodes.append(trans[i])
        
    for i in range(1, len(nodes), 2):
        if (len(tree) == 0):
            tree.append([nodes[i], nodes[i-1]])
            continue
    
        index1 = getIndexOfBranch(tree,nodes[i])
        index2 = getIndexOfBranch(tree,nodes[i - 1])
        
        if (index1 == index2 and index1 != -1):
            continue
        
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
            tree[index2].append(nodes[i])
        else:
            tree[index2].append(nodes[i-1])
            
    if len(tree) != 1:
        Warnings.unreachableStates()
 
 
def checkDisjoint(trans):
    nodes = []
    for i in range(len(trans)):
        if i % 3 != 1:
            nodes.append(trans[i])
    for i in range(1, len(nodes), 2):
        if (nodes[i] == nodes[i - 1]):
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


def isFsaComplete(alphas, trans):
    nodes = set()
    cons = {}

    for i in range(len(trans)):
        if i % 3 != 1:
            nodes.add(trans[i])
    
    for i in nodes:
        cons[i] = set()
        
    for i in range(0, len(trans), 3):
        cons[trans[i]].add(trans[i + 1])
        cons[trans[i + 2]].add(trans[i + 1])

    setAl = set(alphas)
    for vals in cons.values():
        if  vals != setAl:
            return False
    return True

def writeFsaIsComplete(val):
    stream = open("result.txt", "w")
    if val:
        stream.write("FSA is complete")
    else:
        stream.write("FSA is incomplete")
    stream.close()
    

def checkAcceptingState(fins):
    if len(fins) == 0:
        Warnings.undefinedAcceptedState()


def validate(data: list):
    
    states = data[0]
    alphas = data[1]
    inits = data[2]
    fins = data[3]
    trans = data[4]
    
    checkStates(states, inits, fins, trans)
    
    checkInitState(inits)
    
    checkAlphabet(trans, alphas)
    
    checkDisjoint(trans)
    
    writeFsaIsComplete(isFsaComplete(alphas, trans))
    
    checkAcceptingState(fins)
    
    checkReachability(inits,trans)


def main():
    stream = open("fsa.txt", "r")
    data = stream.readlines()
    stream.close()
    
    data = parse(data)
    
    validate(data)

main()