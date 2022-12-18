get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

class Rock:
    def __init__(self, shape):
        self.shape = shape

    def GetHeight(self):
        return len(self.shape[0])

    def GetWidth(self):
        return len(self.shape)

    def DoesRockOverlapWithMap(self, map, lowerLeft):
        if lowerLeft[0] < 0 or lowerLeft[1] < 0 or lowerLeft[0] + self.GetWidth() > len(map) or lowerLeft[1] + self.GetHeight() > len(map[0]):
            return True
        
        for x in range(lowerLeft[0], lowerLeft[0] + self.GetWidth()):
            for y in range(lowerLeft[1], lowerLeft[1] + self.GetHeight()):
                shapex = x - lowerLeft[0]
                shapey = y - lowerLeft[1]

                if map[x][y] == 1 and self.shape[shapex][shapey] == 1:
                    return True

        return False
    
    def DrawRockOnMap(self, map, lowerLeft, val=1):
        for x in range(lowerLeft[0], lowerLeft[0] + self.GetWidth()):
            for y in range(lowerLeft[1], lowerLeft[1] + self.GetHeight()):
                shapex = x - lowerLeft[0]
                shapey = y - lowerLeft[1]

                if self.shape[shapex][shapey] == 1:
                    map[x][y] = val
    
    def FitsThruTopLayer(self, map):
        layerToCheck = GetMaxHeight(map) - 1
        for x in range(len(map)):
            checkPos = (x, layerToCheck)
            if not self.DoesRockOverlapWithMap(map, checkPos):
                return True
        return False

def DrawMap(map, maxHeight = 100):
    toDraw = ""
    if len(map[0]) <= maxHeight:
        maxHeight = len(map[0]) + 1

    for y in range(len(map[0])-1, len(map[0])-maxHeight, -1):
        for x in range(len(map)):
            if not map[x][y]:
                toDraw += "."
            elif map[x][y] == 1:
                toDraw += "#"
            else:
                toDraw += "@"
        toDraw += "\n"
    print(toDraw)

def CopyMap(map):
    copy = []
    for i in range(len(map)):
        copy.append(map[i].copy())
    return copy

def GetMaxHeight(map):
    for y in range(len(map[0])-1, -1, -1):
        for x in range(len(map)):
            if map[x][y] == 1:
                return y + 1

    return 0

def ReduceMap(map):
    reduced = [[map[i][len(map[i])-1000:]] for i in range(len(map))]

    return (reduced, len(map[0]) - len(reduced))
        
rocks = []

rocks.append(Rock([
    [1],
    [1],
    [1],
    [1]]
))
rocks.append(Rock([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]]
))
rocks.append(Rock([
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1]]
))
rocks.append(Rock([
    [1, 1, 1, 1]]
))
rocks.append(Rock([
    [1,1],
    [1,1]]
))

data = get_input("data/Day17Data.txt")[0]

caveWidth = 7

map = [[0] for i in range(caveWidth)]

numRocks = 1000000000000
#numRocks = 2022

maxHeight = 0
jetPos = 0
totalCut = 0

possibleCycleStarts = dict()

cycleFound = False
numRocksInCycle = 0
cycleHeight = 0
numCycles = 0

i = 0
while i < numRocks and not cycleFound:
    print(i)
    rockToDrop = rocks[i % len(rocks)]

    if not rockToDrop.FitsThruTopLayer(map):
        if (i%len(rocks), jetPos) in possibleCycleStarts.keys():
            numRocksInCycle = i - possibleCycleStarts[(i%len(rocks), jetPos)][0]
            cycleHeight = GetMaxHeight(map) - possibleCycleStarts[(i%len(rocks), jetPos)][1]
            while i + numRocksInCycle < numRocks: # while we're able to fit another cycle in, do it
                numCycles += 1
                i += numRocksInCycle
        else:
            possibleCycleStarts[(i%len(rocks), jetPos)] = (i, GetMaxHeight(map))

    # expand the map if we need to
    while len(map[0]) < maxHeight + 3 + rockToDrop.GetHeight():
        for j in range(len(map)):
            map[j].append(0)

    dropPos = (2, maxHeight + 3)

    rockSettled = False

    while not rockSettled:
        # push with air jet
        newPos = None
        if data[jetPos] == ">":
            newPos = (dropPos[0] + 1, dropPos[1])
        elif data[jetPos] == "<":
            newPos = (dropPos[0] - 1, dropPos[1])

        if not rockToDrop.DoesRockOverlapWithMap(map, newPos):
            dropPos = newPos

        jetPos = (jetPos + 1) % len(data)
        # drop rock down
        nextPos = (dropPos[0], dropPos[1] - 1)
        if rockToDrop.DoesRockOverlapWithMap(map, nextPos):
            rockToDrop.DrawRockOnMap(map, dropPos)
            rockSettled = True
            maxHeight = GetMaxHeight(map)
        else:
            dropPos = nextPos

    i += 1

print(maxHeight)
print()
print(GetMaxHeight(map) + numCycles * cycleHeight)
