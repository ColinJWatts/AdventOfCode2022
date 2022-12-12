data = open("data/Day8Data.txt", 'r').readlines()

def UpdateVisible_LookUp(trees, visible):
    maxHeights = []
    for i in range(len(trees)):
        maxHeights.append(trees[i][-1])
        visible[i][-1] = 1

    for x in range(len(trees)):
        for y in range(len(trees[x])-1, -1, -1):
            if trees[x][y] > maxHeights[x]:
                maxHeights[x] = trees[x][y]
                visible[x][y] = 1

def UpdateVisible_LookDown(trees, visible):
    maxHeights = []
    for i in range(len(trees)):
        maxHeights.append(trees[i][0])
        visible[i][0] = 1

    for x in range(len(trees)):
        for y in range(len(trees[x])):
            if trees[x][y] > maxHeights[x]:
                maxHeights[x] = trees[x][y]
                visible[x][y] = 1

def UpdateVisible_LookRight(trees, visible):
    maxHeights = []
    for i in range(len(trees[0])):
        maxHeights.append(trees[0][i])
        visible[0][i] = 1

    for x in range(len(trees)):
        for y in range(len(trees[x])):
            if trees[x][y] > maxHeights[y]:
                maxHeights[y] = trees[x][y]
                visible[x][y] = 1

def UpdateVisible_LookLeft(trees, visible):
    maxHeights = []
    for i in range(len(trees[-1])):
        maxHeights.append(trees[-1][i])
        visible[-1][i] = 1

    for x in range(len(trees)-1, -1, -1):
        for y in range(len(trees[x])):
            if trees[x][y] > maxHeights[y]:
                maxHeights[y] = trees[x][y]
                visible[x][y] = 1

#part 2
def GetScenicScoreForLocation(trees, x, y):
    h = trees[x][y]

    # look up
    upVal = 0
    iter = y-1
    finished = False
    while iter >= 0 and not finished:
        upVal += 1
        if trees[x][iter] >= h:
            finished = True
        iter -= 1

    # look down
    downVal = 0
    iter = y+1
    finished = False
    while iter < len(trees[x]) and not finished:
        downVal += 1
        if trees[x][iter] >= h:
            finished = True
        iter += 1

    # look left
    leftVal = 0
    iter = x-1
    finished = False
    while iter >= 0 and not finished:
        leftVal += 1
        if trees[iter][y] >= h:
            finished = True
        iter -= 1

    # look right
    rightVal = 0
    iter = x+1
    finished = False
    while iter < len(trees) and not finished:
        rightVal += 1
        if trees[iter][y] >= h:
            finished = True
        iter += 1

    return upVal * downVal * leftVal * rightVal

def PrintGrid(grid):
    toprint=""

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            toprint = toprint + f"{grid[x][y]}"
        toprint += "\n"

    print(toprint)

# this is assuming that the data is square
trees = [[0 for j in range(len(data))] for i in range(len(data))]
visibleMask = [[0 for j in range(len(data))] for i in range(len(data))]
sc = [[0 for j in range(len(data))] for i in range(len(data))]

for y in range(len(data)):
    dat = data[y].strip()
    for x in range(len(dat)):
        trees[x][y] = dat[x]

UpdateVisible_LookUp(trees, visibleMask)
UpdateVisible_LookDown(trees, visibleMask)
UpdateVisible_LookRight(trees, visibleMask)
UpdateVisible_LookLeft(trees, visibleMask)

PrintGrid(trees)
PrintGrid(visibleMask)

max = 0

for x in range(len(trees)):
    for y in range(len(trees[x])):
        score = GetScenicScoreForLocation(trees, x, y)
        sc[x][y] = score
        if score > max:
            max = score

totalVisible = 0
for x in range(len(visibleMask)):
    totalVisible += sum(visibleMask[x])

print(totalVisible)

print(f"Max Scenic Score: {max}")