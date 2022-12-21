import operator

get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

class Monkey:
    def __init__(self, startingItems, operationLambda, testLambda, targetA, targetB):
        self.heldItems = startingItems
        self.modulo = 10 # will set this later
        self.Operation = operationLambda
        self.Test = testLambda
        self.totalInspections = 0
        self.targetA = targetA
        self.targetB = targetB

    def TakeTurn(self):
        updatedItems = []
        targets = []

        for item in self.heldItems:
            updated = self.Operation(item)
            #updated = int(updated/3)
            if updated >= self.modulo:
                updated = updated % self.modulo
            updatedItems.append(updated)

            if self.Test(updated):
                targets.append(self.targetA)
            else:
                targets.append(self.targetB)

            self.totalInspections += 1
        
        self.heldItems = []
        return updatedItems, targets


def ParseMonkey(raw):
    # Parse the items the monkey is holding
    startingItems = [int(x.strip()) for x in raw[1][len("  Starting items:"):].split(",")]
    
    # Parse relevent info for the operator
    # Operators are assumed to have the form 'new = old [operation] [value]'
    # current supported operations are [+, *]
    # value can be an integer or 'old' 
    temp = raw[2][len("  Operation: new = old "):].split(" ")
    op = None
    if temp[0] == "+":
        op = operator.add
    elif temp[0] == "*":
        op = operator.mul

    operation = None
    if temp[1] == "old":
        operation = lambda x: op(x, x)
    else:
        val = int(temp[1])
        operation = lambda x: op(x, val)

    # Parse the info for the test
    testVal = int(raw[3][len("  Test: divisible by "):])
    testLambda = lambda x : x % testVal == 0

    # Parse targets
    targetA = int(raw[4][len("    If true: throw to monkey "):])
    targetB = int(raw[5][len("    If false: throw to monkey "):])

    return Monkey(startingItems, operation, testLambda, targetA, targetB), testVal

data = get_input("data/Day11Data.txt")

monkeyData = []
monkeys = []

totalModulo = 1

for d in data:
    if d != "":
        monkeyData.append(d)

    if len(monkeyData) == 6:
        m, testVal = ParseMonkey(monkeyData)
        monkeys.append(m)
        totalModulo = totalModulo * testVal
        monkeyData = []

for m in monkeys:
    m.modulo = totalModulo

numRounds = 10000

for i in range(numRounds):
    for m in monkeys:
        updatedItems, targets = m.TakeTurn()

        for j in range(len(updatedItems)):
            monkeys[targets[j]].heldItems.append(updatedItems[j])

l = []
for m in monkeys:
    l.append(m.totalInspections)
    print(f"{m.totalInspections}: {m.heldItems}")
print("")
l.sort()
print(l[-1] * l[-2])