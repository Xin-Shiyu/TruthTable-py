import LogicUtilities

def GetBit(val : int, place : int) -> bool:
    return ((val >> place) & 1) == 1

def Main():
    print("TruthTable By Xin Shiyu")
    print("Please enter an expression,\n" +
        "! stands for not, & stands for and, and | stands for or.\n" +
        "Use lowercase letters as variables.\n" +
        "Parentheses can be used as well.")
    while (True):
        exp : str = input()
        if (len(exp) == 0):
            break
        dct = {}
        tree = LogicUtilities.Parser.Parse(exp, dct)
        table = [[]]
        expPlaceList = []
        count : int = 0
        def makeTruthDict(node):
            nonlocal count
            nonlocal expPlaceList
            nonlocal table
            count += 1
            table[0].append(node.__str__())
            expPlaceList.append(node)
            if (isinstance(node, LogicUtilities.Compound)):
                for x in node.Children:
                    makeTruthDict(x)
        makeTruthDict(tree)
        for i in range(1 << len(dct)):
            table.append([])
            j : int = 0
            for key in dct:
                dct[key].Truth = GetBit(i, j)
                j += 1
            for e in expPlaceList:
                table[-1].append("T" if e.Evaluate() else "F")
        for row in table:
            for col in row:
                print(col, end = " ")
            print()