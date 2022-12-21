import operator

get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day21Data.txt")

class Monkey:
    def __init__(self, name, value, operation, leftMonkey, rightMonkey):
        self.name = name
        self.value = value
        self.operation = operation
        self.leftMonkey = leftMonkey
        self.rightMonkey = rightMonkey
        
    def GetValue(self, monkiesByName):
        if not self.value is None:
            return self.value

        l = monkeiesByName[self.leftMonkey].GetValue(monkeiesByName)
        r = monkeiesByName[self.rightMonkey].GetValue(monkeiesByName)

        return self.operation(l, r)

    def IsHumnInPath(self, monkiesByName):
        if self.name == "humn":
            return True

        if not self.value is None:
            return False

        return monkiesByName[self.leftMonkey].IsHumnInPath(monkiesByName) or monkiesByName[self.rightMonkey].IsHumnInPath(monkiesByName)

    def Reverse(self, monkiesByName, currentVal):
        if self.name == "humn":
            print(f"Part 2 Solution: {currentVal}")
            return
    
        if self.operation == operator.add:
            if monkiesByName[self.leftMonkey].IsHumnInPath(monkiesByName):
                monkiesByName[self.leftMonkey].Reverse(monkiesByName, currentVal - monkiesByName[self.rightMonkey].GetValue(monkiesByName))
            else:
                monkiesByName[self.rightMonkey].Reverse(monkiesByName, currentVal - monkiesByName[self.leftMonkey].GetValue(monkiesByName))
        elif self.operation == operator.sub:
            if monkiesByName[self.leftMonkey].IsHumnInPath(monkiesByName):
                monkiesByName[self.leftMonkey].Reverse(monkiesByName, currentVal + monkiesByName[self.rightMonkey].GetValue(monkiesByName))
            else:
                monkiesByName[self.rightMonkey].Reverse(monkiesByName, monkiesByName[self.leftMonkey].GetValue(monkiesByName) - currentVal)
        elif self.operation == operator.mul:
            if monkiesByName[self.leftMonkey].IsHumnInPath(monkiesByName):
                monkiesByName[self.leftMonkey].Reverse(monkiesByName, currentVal / monkiesByName[self.rightMonkey].GetValue(monkiesByName))
            else:
                monkiesByName[self.rightMonkey].Reverse(monkiesByName, currentVal / monkiesByName[self.leftMonkey].GetValue(monkiesByName))
        elif self.operation == operator.floordiv:
            if monkiesByName[self.leftMonkey].IsHumnInPath(monkiesByName):
                monkiesByName[self.leftMonkey].Reverse(monkiesByName, currentVal * monkiesByName[self.rightMonkey].GetValue(monkiesByName))
            else:
                monkiesByName[self.rightMonkey].Reverse(monkiesByName, monkiesByName[self.leftMonkey].GetValue(monkiesByName) / currentVal)

monkeiesByName = {}
rootMonkey = None

for d in data:
    [monkeyName, job] = d.split(":")
    job = job.strip()

    val = None
    operation = None
    leftMonkey = None
    rightMonkey = None
    try:
        val = int(job)
    except:
        # here we parse out the job
        [leftMonkey, op, rightMonkey] = job.split(" ")
        if op == "+":
            operation = operator.add
        elif op == "-":
            operation = operator.sub
        elif op == "/":
            operation = operator.floordiv
        elif op == "*":
            operation = operator.mul

    m = Monkey(monkeyName, val, operation, leftMonkey, rightMonkey)
    monkeiesByName[monkeyName] = m
    if monkeyName == "root":
        rootMonkey = m

#humn is on the left of the root monkey op
rVal = monkeiesByName[rootMonkey.rightMonkey].GetValue(monkeiesByName)
print(rVal)

monkeiesByName[rootMonkey.leftMonkey].Reverse(monkeiesByName, rVal)
