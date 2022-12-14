get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day14Data.txt")

maxX = 0
minX = 100000000000
maxY = 0
minY = 100000000000

def PrintRocks(rockSet, sandSet, minXY, maxXY):
    if minXY[1] > 0:
        minXY = (minXY[0], 0)
    
    offset = maxXY[0] - minXY[0]
    vals = [['.' for y in range(maxXY[1])] for x in range(offset)]

    for x in range(offset):
        for y in range(maxXY[1] - minXY[1]):
            if (x + minXY[0], y) in rockSet and (x + minXY[0], y) in sandSet:
                raise Exception("Sand and rock overlapping")
            if (x + minXY[0], y) in rockSet:
                vals[x][y] = "#"
            if (x + minXY[0], y) in sandSet:
                vals[x][y] = "o"

    toPrint = ""
    for y in range(len(vals[0])):
        for x in range(len(vals)):
            toPrint += vals[x][y]
        toPrint += "\n"
    print(toPrint)

def AddToRockSet(rockSet, start, end):
    if start[0] != end[0] and start[1] != end[1]:
        print("INVALID DATA") # we can only add straight lines
        return

    if start[0] == end[0]: 
        # vertical line of rocks
        if start[1] > end[1]:
            #switch where we start adding from
            temp = start
            start = end
            end = temp

        for i in range(start[1], end[1] + 1):
            if not (start[0], i) in rockSet:
                rockSet.add((start[0], i))
        return
    
    if start[1] == end[1]:
        # horizontal line of rocks
        if start[0] > end[0]:
            #switch where we start adding from
            temp = start
            start = end
            end = temp
        for i in range(start[0], end[0] + 1):
            if not (i, start[1]) in rockSet:
                rockSet.add((i, start[1]))
        return

# returns true when sand comes to rest
# returns false when sand falls off map
def DropSand(rockSet, sandSet, maxXY, dropLoc=500):
    sandPos = (dropLoc, -1)
    
    while True:
        down = (sandPos[0], sandPos[1] + 1)
        downL = (sandPos[0] - 1, sandPos[1] + 1)
        downR = (sandPos[0] + 1, sandPos[1] + 1)

        if not down in rockSet and not down in sandSet:
            sandPos = down
        elif not downL in rockSet and not downL in sandSet:
            sandPos = downL
        elif not downR in rockSet and not downR in sandSet:
            sandPos = downR
        else:
            # sand is at rest
            sandSet.add(sandPos)
            if sandPos == (dropLoc, 0):
                return False
            return True

        if sandPos[1] > maxXY[1]:
                return False

rockSet = set()
sandSet = set()

for d in data:
    rockFormations = d.split("->")
    corners = []
    for corner in rockFormations:
        temp = corner.strip().split(",")
        temp[0] = int(temp[0])
        temp[1] = int(temp[1])
        corners.append(temp)

        # get max and min bounds of the rock
        if temp[0] > maxX:
            maxX = temp[0]
        if temp[0] < minX:
            minX = temp[0]
        if temp[1] > maxY:
            maxY = temp[1]
        if temp[1] < minY:
            minY = temp[1]
    
    for i in range(len(corners) - 1):
        AddToRockSet(rockSet, corners[i], corners[i+1])

floorSize = 500

AddToRockSet(rockSet, (minX - floorSize, maxY + 2), (maxX + floorSize, maxY + 2))
minX = minX - floorSize
maxX = maxX + floorSize
maxY = maxY + 3

PrintRocks(rockSet, sandSet, (minX, minY), (maxX+1, maxY+1))

sandCount = 0

while DropSand(rockSet, sandSet, (maxX+1, maxY+1)):
    sandCount += 1
    #PrintRocks(rockSet, sandSet, (minX, minY), (maxX+1, maxY+1))
    
print(f"Number of Sands dropped: {sandCount}")