
class Errors:
    output = "result.txt"

    @staticmethod    
    def E1(state):
        stream = open(Errors.output, "a")
        stream.write(f"Error:\nE1: A state '{state}' is not in the set of states")
        stream.close()
        exit(0)

    @staticmethod  
    def E2():
        stream = open(Errors.output, "a")
        stream.write("Error:\nE2: Some states are disjoint")
        stream.close()
        exit(0)

    @staticmethod  
    def E3(trans):
        stream = open(Errors.output, "a")
        stream.write(f"Error:\nE3: A transition '{trans}' is not represented in the alphabet")
        stream.close()
        exit(0)

    @staticmethod  
    def E4():
        stream = open(Errors.output, "a")
        stream.write("Error:\nE4: Initial state is not defined")
        stream.close()
        exit(0)

    @staticmethod  
    def E5():
        stream = open(Errors.output, "a")
        stream.write("Error:\nE5: Input file is malformed")
        stream.close()
        exit(0)

class Warnings:

    output: str = "result.txt"
    
    @staticmethod
    def W1():
        stream = open(Errors.output, "a")
        stream.write("W1: Accepting state is not defined")
        stream.close()
        
    @staticmethod
    def W2():
        stream = open(Errors.output, "a")
        stream.write("W2: Some states are not reachable from the initial state")
        stream.close()

    @staticmethod
    def W2():
        stream = open(Errors.output, "a")
        stream.write("W3: FSA is nondeterministic")
        stream.close()

def parse(data: list):
    if (len(data) != 5):
        Errors.E5()
        
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
        
        if (len(data[i]) == 0):
            data[i] = []
        else:
            data[i] = data[i]
            
    
    return data;


def main():
    stream = open("result.txt", "w")
    stream.close();
    
    try:
        stream = open("fsa.txt")
        data = stream.readlines()
        stream.close()
    except:
        Errors.E5()
    
    data = parse(data)
    
    statesAllowedSymbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    alphasAllowedSymbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    
    states = data[0]
    alphas = data[1]
    inits = data[2]
    fins = data[3]
    trans = data[4]
    
    for st in states:
        for s in st:
            if s not in statesAllowedSymbols:
                Errors.E5()
                
    for al in alphas:
        for s in al: 
            if s not in alphasAllowedSymbols:
                Errors.E5()
    
    if (len(inits) == 0):
        Errors.E4()
    
    for i in range(1, len(trans), 3):
        if trans[i] not in alphas:
            Errors.E3(trans[i])
    
    for i in range(0, len(trans), 3):
        if trans[i] not in states:
            Errors.E1(trans[i])
    
main();

asd