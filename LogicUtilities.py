from enum import Enum

class Stack(object):
    __array = []

    def Push(self, newValue):
        self.__array.append(newValue)

    def Pop(self):
        return self.__array.pop()

    def Peek(self):
        return self.__array[-1]

    @property
    def Count(self):
        return len(self.__array)


class OperatorType(Enum):
    AND = 1,
    OR = 2,
    NOT = 3,
    IMP = 4,
    DCON = 5


class Compound:
    Type : OperatorType
    Children = []

    @property
    def Truth(self) -> bool:
        self.Evaluate()
    
    def Evaluate(self) -> bool:
        if (self.Type == OperatorType.NOT):
            return not self.Children[0].Evaluate()
        elif (self.Type == OperatorType.AND):
            return self.Children[0].Evaluate() and self.Children[1].Evaluate()
        elif (self.Type == OperatorType.OR):
            return self.Children[0].Evaluate() or self.Children[1].Evaluate()
        elif (self.Type == OperatorType.IMP):
            return not self.Children[0].Evaluate or self.Children[1].Evaluate()
        elif (self.Type == OperatorType.DCON):
            return self.Children[0] == self.Children[1]

    def __init__(self, type : OperatorType):
        self.Type = type

    def __str__(self):
        if (self.Type == OperatorType.NOT):
            return "(!" + self.Children[0].__str__() + ")"
        elif (self.Type == OperatorType.AND):
            return "(" + self.Children[0].__str__()  + "&" + self.Children[1].__str__()  + ")"
        elif (self.Type == OperatorType.OR):
            return "(" + self.Children[0].__str__()  + "|" + self.Children[1].__str__()  + ")"
        elif (self.Type == OperatorType.IMP):
            return "(" + self.Children[0].__str__()  + "->" + self.Children[1].__str__() + ")"
        elif (self.Type == OperatorType.DCON):
            return "(" + self.Children[0].__str__()  + "<->" + self.Children[1].__str__()  + ")"


class Atom:
    Name : str
    Truth : bool = None

    def __init__(self, *args):
        if (len(args) >= 1):
            self.Name = args[0]
            if (len(args) == 2):
                self.Truth = args[1]

    def Evaluate(self) -> bool:
        if (self.Truth == None):
            raise Exception("Truth of atom not determined.")
        else:
            return self.Truth

    def __str__(self):
        return self.Name


class Parser:
    @staticmethod
    def __ToPostfix(s : str):
        stack = Stack()
        res = []
        lastChar= '\0'
        lastB2Char = '\0'
        for c in s:
            if (c == '('):
                stack.Push("(")
            elif (c == ')'):
                while (stack.Count != 0 and stack.Peek() != "("):
                    res.append(stack.Pop())
                if (stack.Count != 0 and stack.Peek() == "("):
                    stack.Pop()
            elif (c == '!'):
                stack.Push("!")
            elif (c == '&'):
                while (stack.Count != 0 and stack.Peek() == "!"):
                    res.append(stack.Pop())
                stack.Push("&")
            elif (c == '|'):
                while (stack.Count != 0 and (stack.Peek() == "&" or stack.Peek() == "!")):
                    res.append(stack.Pop())
                stack.Push("|")
            elif (c == '>'):
                if (lastChar == '-'):
                    if (lastB2Char == '<'):
                        while (stack.Count != 0 and (stack.Peek() == "&" or stack.Peek() == "|" or stack.Peek() == "->" or stack.Peek() == "!")):
                            res.append(stack.Pop())
                        stack.Push("<->")
                    else:
                        while (stack.Count != 0 and (stack.Peek() == "&" or stack.Peek() == "|" or stack.Peek() == "!")):
                            res.append(stack.Pop())
                        stack.Push("->")
            elif (c != '<' and c != '-'):
                res.append(c)
            lastB2Char = lastChar
            lastChar = c
        while (stack.Count != 0):
            res.append(stack.Pop())
        return res

    @staticmethod
    def __CreateTreeFromList(lst : list, dct : dict):
        stackProp = Stack()
        for token in lst:
            if (token == "&"):
                temp = Compound(OperatorType.AND)
                temp.Children = [stackProp.Pop(), stackProp.Pop()]
                stackProp.Push(temp)
            elif (token == "|"):
                temp = Compound(OperatorType.OR)
                temp.Children = [stackProp.Pop(), stackProp.Pop()]
                stackProp.Push(temp)
            elif (token == "!"):
                temp = Compound(OperatorType.NOT)
                temp.Children = [stackProp.Pop()]
                stackProp.Push(temp)
            elif (token == "->"):
                prop2 = stackProp.Pop()
                prop1 = stackProp.Pop()
                temp = Compound(OperatorType.IMP)
                temp.Children = [prop1, prop2]
                stackProp.Push(temp)
            elif (token == "<->"):
                temp = Compound(OperatorType.DCON)
                temp.Children = [stackProp.Pop(), stackProp.Pop()]
                stackProp.Push(temp)
            else:
                if (dct[token[0]] != None):
                    stackProp.Push(dct[token[0]])
                else:
                    dct[token[0]] = Atom(token[0])
                    stackProp.Push(dct[token[0]])
        return stackProp.Pop()

    @staticmethod
    def Parse(exp : str, dct : dict):
        map = [False for _ in range(26)]
        for c in exp:
            if 97 <= ord(c) <= 122 and not map[ord(c) - 97]:
                map[ord(c) - 97] = True
                dct[c] = None
        return Parser.__CreateTreeFromList(Parser.__ToPostfix(exp), dct)