get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

def PrintGrid(grid):
    toprint=""
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            toprint = toprint + f"{grid[x][y]}"
        toprint += "\n"

    print(toprint)

def GetHeight(item): 
    if item.isupper():
        if item == "S":
            return 1
        if item == "E":
            return 26
    else:
        return ord(item) - ord('a') + 1

def IsValidPos(map, x, y):
    return x >= 0 and x < len(map) and y >= 0 and y < len(map[x])

def IsMoveValid(source, dest):
    return dest <= source + 1

class Node:
    def __init__(self, map, x, y):
        self.height = GetHeight(map[x][y])
        self.neighbors = []

        if IsValidPos(map, x + 1, y) and IsMoveValid(self.height, GetHeight(map[x + 1][y])):
            self.neighbors.append((x + 1, y))

        if IsValidPos(map, x, y - 1) and IsMoveValid(self.height, GetHeight(map[x][y - 1])):
            self.neighbors.append((x, y - 1))

        if IsValidPos(map, x - 1, y) and IsMoveValid(self.height, GetHeight(map[x - 1][y])):
            self.neighbors.append((x - 1, y))

        if IsValidPos(map, x, y + 1) and IsMoveValid(self.height, GetHeight(map[x][y + 1])):
            self.neighbors.append((x, y + 1))

def BFS (nodes, start, end):
    toSearch = [start]
    paths = [[]]
    visited = []

    while toSearch:
        m = toSearch.pop(0)
        p = paths.pop(0)
        if not m in visited:
            visited.append(m)
            p.append(m)
            if m == end:
                return p

            for n in nodes[m].neighbors:
                toSearch.append(n)
                paths.append(p.copy())


data = get_input("data/Day12Data.txt")

map = [[0 for j in range(len(data))] for i in range(len(data[0]))]
nodes = {}

startPos = None
endPos = None
lowestElevations = []

for y in range(len(data)):
    for x in range(len(data[y])):
        map[x][y] = data[y][x]
        if map[x][y] == "S":
            startPos = (x, y)
            lowestElevations.append((x, y))
        if map[x][y] == "E":
            endPos = (x, y)
        if map[x][y] == "a":
            lowestElevations.append((x, y))

for x in range(len(map)):
    for y in range(len(map[x])):
        nodes[(x, y)] = Node(map, x, y)

#PrintGrid(map)

lengths = []
for l in lowestElevations:
    path = BFS(nodes, l, endPos)
    if not path is None:
        lengths.append(len(path) - 1)

lengths.sort()
print(lengths)
