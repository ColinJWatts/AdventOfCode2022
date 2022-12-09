class StackSetup:
    def __init__(self, rawLines):
        self.rawLines = rawLines

        self.stacks = []
        for i in range(len(self.rawLines[-1].split("   "))):
            self.stacks.append([])

        for i in range(len(self.rawLines)-2, -1, -1):
            line = self.rawLines[i].split(" ")
            stackNum = 0
            j = 0
            while j < len(line):
                if line[j].strip() != "":
                    self.stacks[stackNum].append(line[j].strip().replace('[', '').replace(']', ''))
                    j += 1
                else:
                    j += 4
                stackNum += 1

    def MoveOneCrate(self, sourceStack, targetStack):
        if sourceStack < 0 or sourceStack >= len(self.stacks) or len(self.stacks[sourceStack]) == 0:
            print("Something went wrong")
            input() #catch it here for debugging

        if targetStack < 0 or targetStack >= len(self.stacks):
            print("Something went wrong")
            input() #catch it here for debugging
        
        val = self.stacks[sourceStack].pop()
        self.stacks[targetStack].append(val)

    def MoveNCrates(self, sourceStack, targetStack, n):
        for i in range(len(self.stacks[sourceStack]) - n, len(self.stacks[sourceStack])):
            self.stacks[targetStack].append(self.stacks[sourceStack][i])
        self.stacks[sourceStack] = self.stacks[sourceStack][:len(self.stacks[sourceStack]) - n]

    def PrintTopLevel(self):
        result = ""
        for s in self.stacks:
            if len(s) > 0:
                result += s[-1]
            else:
                result += "_"

        print(result)

data = open("data/Day5Data.txt", 'r').readlines()

stackData = []
i=0
while data[i].strip() != "":
    stackData.append(data[i].strip())
    i+=1

i+=1
stacks = StackSetup(stackData)

while i < len(data):
    #get instruction
    #execute on stacks
    temp = data[i].strip()[5:].split(" from ")

    numToMove = int(temp[0])

    temp = temp[1].split(" to ")
    source = int(temp[0]) - 1
    target = int(temp[1]) - 1

    # for j in range(numToMove):
    #     stacks.MoveOneCrate(source, target)
    stacks.MoveNCrates(source, target, numToMove)

    i+=1 

print(stacks.stacks)
stacks.PrintTopLevel()