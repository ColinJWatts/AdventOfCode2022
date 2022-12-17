get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day16Data.txt")

class Node:
    def __init__(self, name, flowRate, neighborNames):
        self.name = name
        self.flowRate = flowRate
        self.neighbors = neighborNames
        self.isOpen = False

    def Copy(self):
        newNode = Node(self.name, self.flowRate, self.neighbors.copy())
        newNode.isOpen = self.isOpen
        return newNode

def CopyNodes(nodes):
    nodeCopy = {}

    for key in nodes.keys():
        nodeCopy[key] = nodes[key].Copy()

    return nodeCopy

def FindInstantaniousFlow(nodes):
    sum = 0
    for key in nodes.keys():
        if nodes[key].isOpen:
            sum += nodes[key].flowRate
    return sum

def GetActions(nodes, currentLoc, maxPossibleFlow):
    actions = []

    if FindInstantaniousFlow(nodes) == maxPossibleFlow:
        return [currentLoc]

    if not nodes[currentLoc].isOpen:
        actions.append("open")

    for n in nodes[currentLoc].neighbors:
        actions.append(n)
    return actions

nodes = {}

for d in data:
    valveName = d.split(" ")[1]
    remainder = d.split("=")[1]
    flowRate =  int(remainder.split(";")[0])
    connections = remainder.split(";")[1].replace(",", "").split(" ")[5:]
    nodes[valveName] = Node(valveName, flowRate, connections)

minute = 0
startingPos = ["AA"]
currNodes = [nodes]
totalFlows = [0]
instantFlows = [0]
visited = [[]]

maxFlowRate = 0
for key in nodes.keys():
    maxFlowRate += nodes[key].flowRate

maxTotalFlow = 0
maxInstantaniousFlow = 0

while minute < 30:
    print(f"minute {minute} has {len(startingPos)} paths to check")
    nextStartingPos = []
    nextNodes = []
    updatedTotalFlows = []
    updatedInstantFlows = []
    updatedVisited = []

    pathsCut = 0

    tempMax = 0
    tempInst = 0

    uniqueEndpoints = set()

    while startingPos:
        # get our next path to check 
        currPos = startingPos.pop(0)
        n = currNodes.pop(0)
        currentTotalFlow = totalFlows.pop(0)
        currentInstantFlow = instantFlows.pop(0)
        currentVisited = visited.pop(0)

        currentVisited.append((currPos, currentInstantFlow))

        if (currPos, currentInstantFlow) in uniqueEndpoints:
            pathsCut += 1
            continue

        uniqueEndpoints.add((currPos, currentInstantFlow))

        # heuristics to cut down on number of paths to search
        if minute >= 10 and currentTotalFlow == 0:
            pathsCut += 1
            continue

        if currentTotalFlow + maxFlowRate * (30 - minute) < maxTotalFlow + maxInstantaniousFlow * (30 - minute):
            pathsCut += 1
            continue

        actions = GetActions(n, currPos, maxFlowRate)
        for action in actions:
            if action == "open" and n[currPos].flowRate == 0:
                pathsCut += 1
                continue

            if action != "open" and action != currPos and (action, currentInstantFlow) in currentVisited:
                pathsCut += 1
                #print(f"cutting path that goes to visited loc ({action, currentInstantFlow}) from {currPos}")
                continue

            newNodes = CopyNodes(n)

            visitedCopy = currentVisited.copy()

            instantanious = FindInstantaniousFlow(newNodes)
            if instantanious < currentInstantFlow:
                print(f"{instantanious} {currentInstantFlow}")
            updatedTotalFlows.append(currentTotalFlow + instantanious)
            updatedInstantFlows.append(instantanious)

            if updatedTotalFlows[-1] > maxTotalFlow and updatedTotalFlows[-1] > tempMax:
                tempMax = updatedTotalFlows[-1]
                tempInst = instantanious

            if action == "open":
                newNodes[currPos].isOpen = True
                nextStartingPos.append(currPos)
                updatedInstantFlows[-1] += newNodes[currPos].flowRate
            else:
                nextStartingPos.append(action)
            nextNodes.append(newNodes)
            updatedVisited.append(visitedCopy)
            
            if minute >=28:
                print(visitedCopy)
    
    maxTotalFlow = tempMax
    maxInstantaniousFlow = tempInst

    print(f"{pathsCut} paths cut with heuristics")
    startingPos = nextStartingPos
    currNodes = nextNodes
    totalFlows = updatedTotalFlows
    instantFlows = updatedInstantFlows
    visited = updatedVisited
    minute += 1

print(maxTotalFlow)