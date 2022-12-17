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

def GetActions(nodes, currentLoc, currentELoc, maxPossibleFlow):
    actions = []

    if FindInstantaniousFlow(nodes) == maxPossibleFlow:
        return [(currentLoc, currentELoc)]

    personActions = []
    eActions = []

    if not nodes[currentLoc].isOpen:
        personActions.append("open")

    if not nodes[currentELoc].isOpen:
        eActions.append("open")

    for n in nodes[currentLoc].neighbors:
        personActions.append(n)
    
    for n in nodes[currentELoc].neighbors:
        eActions.append(n)

    for a in personActions:
        for e in eActions:
            actions.append((a, e))
 
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
startingPosE = ["AA"]
currNodes = [nodes]
totalFlows = [0]
instantFlows = [0]
visited = [[]]

maxFlowRate = 0
for key in nodes.keys():
    maxFlowRate += nodes[key].flowRate

maxTotalFlow = 0
maxInstantaniousFlow = 0
uniqueEndpoints = set()

while minute < 26:
    print(f"minute {minute} has {len(startingPos)} paths to check")
    nextStartingPos = []
    nextStartingPosE = []
    nextNodes = []
    updatedTotalFlows = []
    updatedInstantFlows = []
    updatedVisited = []

    pathsCut = 0

    tempMax = 0
    tempInst = 0

    while startingPos:
        # get our next path to check 
        currPos = startingPos.pop(0)
        currPosE = startingPosE.pop(0)
        n = currNodes.pop(0)
        currentTotalFlow = totalFlows.pop(0)
        currentInstantFlow = instantFlows.pop(0)
        currentVisited = visited.pop(0)

        currentVisited.append((currPos, currPosE, currentInstantFlow))

        if (currPos, currPosE, currentInstantFlow, currentTotalFlow) in uniqueEndpoints:
            pathsCut += 1
            continue

        uniqueEndpoints.add((currPos, currPosE, currentInstantFlow, currentTotalFlow))
        uniqueEndpoints.add((currPosE, currPos, currentInstantFlow, currentTotalFlow))

        # heuristics to cut down on number of paths to search
        if minute >= 5 and currentTotalFlow == 0:
            pathsCut += 1
            continue

        if minute >= 7 and currentTotalFlow < maxTotalFlow * .95:
            pathsCut += 1
            continue

        if currentTotalFlow + maxFlowRate * (26 - minute) < maxTotalFlow + maxInstantaniousFlow * (26 - minute):
            pathsCut += 1
            continue

        actions = GetActions(n, currPos, currPosE, maxFlowRate)

        for action in actions:
            if (action[0] == "open" and n[currPos].flowRate == 0) or (action[1] == "open" and n[currPosE].flowRate == 0):
                pathsCut += 1
                continue

            if action[0] != "open" and action[0] != currPos and action[1] != "open" and action[1] != currPosE and (action[0], action[1], currentInstantFlow) in currentVisited:
                pathsCut += 1
                continue

            newNodes = CopyNodes(n)

            visitedCopy = currentVisited.copy()

            instantanious = FindInstantaniousFlow(newNodes)

            #debug check
            if instantanious < currentInstantFlow:
                print(f"{instantanious} {currentInstantFlow}")

            updatedTotalFlows.append(currentTotalFlow + instantanious)
            updatedInstantFlows.append(instantanious)

            if updatedTotalFlows[-1] > maxTotalFlow and updatedTotalFlows[-1] > tempMax:
                tempMax = updatedTotalFlows[-1]
                tempInst = instantanious

            if action[0] == "open":
                newNodes[currPos].isOpen = True
                nextStartingPos.append(currPos)
                updatedInstantFlows[-1] += newNodes[currPos].flowRate
            else:
                nextStartingPos.append(action[0])

            if action[1] == "open":
                newNodes[currPosE].isOpen = True
                nextStartingPosE.append(currPosE)
                if not (action[0] == "open" and currPos == currPosE):
                    updatedInstantFlows[-1] += newNodes[currPosE].flowRate
            else:
                nextStartingPosE.append(action[1])

            nextNodes.append(newNodes)
            updatedVisited.append(visitedCopy)
            
            if minute >=25:
                for v in visitedCopy:
                    print(v)
    
    maxTotalFlow = tempMax
    maxInstantaniousFlow = tempInst

    print(f"{pathsCut} paths cut with heuristics")
    startingPos = nextStartingPos
    startingPosE = nextStartingPosE
    currNodes = nextNodes
    totalFlows = updatedTotalFlows
    instantFlows = updatedInstantFlows
    visited = updatedVisited
    minute += 1

print(maxTotalFlow)