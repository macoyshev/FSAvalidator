from gettext import ngettext
import re

# class contains all existing Errors
class Errors:
    output = "output.txt"

    @staticmethod
    def not_deteminisic():
        stream = open(Errors.output, "w")
        stream.write("Error:\nE5: FSA is nondeterministic")
        stream.close()
        exit(0)

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
        stream.write(
            f"Error:\nE3: A transition '{trans}' is not represented in the alphabet"
        )
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
        stream.write("Error:\nE0: Input file is malformed")
        stream.close()
        exit(0)


# parse data: delete unnecessary symbols
def parse(data: list):
    checkFormat(data)

    data[0] = data[0].replace("states=", "")
    data[1] = data[1].replace("alpha=", "")
    data[2] = data[2].replace("initial=", "")
    data[3] = data[3].replace("accepting=", "")
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
            if len(data[i]) == 0:
                data[i] = []
            else:
                data[i] = [data[i]]

    for d in data:
        if d:
            return data

    Errors.malformedInput()


# check that all states in inints, fins and trans are in states
def checkStates(states, inits, fins, trans):
    # checking states in trans
    for i in range(0, len(trans), 3):
        if trans[i] not in states:
            Errors.undefinedState(trans[i])

    # checking states in fins
    for st in fins:
        if st not in states:
            Errors.undefinedState(st)

    # checking states in inits
    for st in inits:
        if st not in states:
            Errors.undefinedState(st)


# init state cannot be empty
def checkInitState(inits):
    if len(inits) == 0:
        Errors.undefinedUnitialState()


# check that all weights in trans were in the alphabet
def checkAlphabet(trans, alphas):
    for i in range(1, len(trans), 3):
        if trans[i] not in alphas:
            Errors.undefinedTransion(trans[i])


# comparing with pattern
def checkFormat(data):
    if len(data) != 5:
        Errors.malformedInput()
    row = ""
    for line in data:
        row += line

    row = row.replace(" ", "")

    pattern = re.compile(
        "states=\[([a-z0-9],?)*\]\nalpha=\[([a-z0-9_],?)*\]\ninitial=\[.*\]\naccepting=\[.*\]\ntrans=\[.*\]"
    )
    result = pattern.findall(row)

    if len(result) == 0:
        Errors.malformedInput()


# represent trans as a graph and if there are some remote branch that means that some states are disjoint
def checkDisjoint(trans):
    d = dict()

    for i in range(0, len(trans), 3):
        d[trans[i]] = True
        d[trans[i + 2]] = True

    for i in range(0, len(trans), 3):
        if trans[i] != trans[i + 2]:
            d[trans[i]] = False
            d[trans[i + 2]] = False

    for val in d.values():
        if val and len(d) != 1:
            Errors.disjointStates()


# support function for checkDisjoint
def isInAnyBranch(tree, node):
    for branch in tree:
        if node in branch:
            return True
    return False


# support function for checkDisjoint
def getIndexOfBranch(tree, node):
    for i in range(len(tree)):
        if node in tree[i]:
            return i

    return -1


# if the state uses all alphas-> complete
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

    setAl = set(alphas)
    for vals in cons.values():
        if vals != setAl:
            return False
    return True


def check_deteministic(trans, alph):
    d = dict()

    for i in range(0, len(trans), 3):
        d[trans[i]] = []
        d[trans[i + 2]] = []

    for i in range(0, len(trans), 3):
        arr = d[trans[i]]
        arr.append(trans[i + 1])
        d[trans[i]] = arr

    for v in d.values():
        if len(v) > len(alph):
            Errors.not_deteminisic()


def get_regex(k, i, j, states, trans, alphas):
    res_str = ""

    if k != -1:
        res_str += "(" + get_regex(k - 1, i, k, states, trans, alphas) + ")"

        res_str += "(" + get_regex(k - 1, k, k, states, trans, alphas) + ")*"

        res_str += "(" + get_regex(k - 1, k, j, states, trans, alphas) + ")|"

        res_str += "(" + get_regex(k - 1, i, j, states, trans, alphas) + ")"

    else:
        was = False

        if i < 0 or j < 0:
            res_str += "{}"

        if i != j:
            for al in alphas:
                if is_sublist([states[i], al, states[j]], trans):
                    res_str += al

                    was = True

            if not was:
                res_str += "{}"
        else:
            for al in alphas:
                if is_sublist([states[i], al, states[j]], trans):
                    res_str += al
                    was = True

                if was:
                    res_str += "|"
                    was = False

            res_str += "eps"

    return res_str


def is_sublist(list1, list2):
    n = len(list1)
    return any((list1 == list2[i : i + n]) for i in range(len(list2) - n + 1))


# union of all checking operations
def validate(data: list):

    states = data[0]
    alphas = data[1]
    inits = data[2]
    fins = data[3]
    trans = data[4]

    checkStates(states, inits, fins, trans)

    checkInitState(inits)

    checkAlphabet(trans, alphas)

    check_deteministic(trans, alphas)

    checkDisjoint(trans)

    stream = open("output.txt", "w")

    if len(fins) == 0:
        stream.write("{}")
    else:
        for i in range(len(fins)):

            stream.write(
                get_regex(
                    len(states) - 1,
                    states.index(inits[0]),
                    states.index(fins[i]),
                    states=states,
                    trans=trans,
                    alphas=alphas,
                )
            )
            if i != len(fins) - 1:
                stream.write("|")


# main
def main():
    stream = open("input.txt", "r")
    data = stream.readlines()
    stream.close()

    data = parse(data)

    validate(data)


main()
