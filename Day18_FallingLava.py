get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day18Data.txt")

cubes = set()

lookDirs = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]

(minx, miny, minz) = (100000, 100000, 100000)
(maxx, maxy, maxz) = (-100000, -100000, -100000)

for d in data:
    cubeLoc = (int(d.split(",")[0]), int(d.split(",")[1]), int(d.split(",")[2]))

    if cubeLoc[0] < minx:
        minx = cubeLoc[0]
    if cubeLoc[1] < miny:
        miny = cubeLoc[1]
    if cubeLoc[2] < minz:
        minz = cubeLoc[2]

    if cubeLoc[0] > maxx:
        maxx = cubeLoc[0]
    if cubeLoc[1] > maxy:
        maxy = cubeLoc[1]
    if cubeLoc[2] > maxz:
        maxz = cubeLoc[2]

    cubes.add(cubeLoc)

total = 0
for cube in cubes:
    for look in lookDirs:
        if not (cube[0] + look[0], cube[1] + look[1], cube[2] + look[2]) in cubes:
            total += 1

print(total)

def updateSets(start, cubeSet):
    toCheck = [start]
    
    currentSet = set()

    isExterior = False
    while toCheck:
        curr = toCheck.pop(0)
        if not curr in cubeSet and not curr in currentSet:
            if curr[0] == minx or curr[0] == maxx or curr[1] == miny or curr[1] == maxy or curr[2] == minz or curr[2] == maxz:
                isExterior = True
            currentSet.add(curr)
            for look in lookDirs:
                next = (curr[0] + look[0], curr[1] + look[1], curr[2] + look[2])
                if not (next[0] < minx or next[0] > maxx or next[1] < miny or next[1] > maxy or next[2] < minz or next[2] > maxz):
                    toCheck.append(next)
    return (isExterior, currentSet)
    

interior = set()
exterior = set()

for x in range(minx, maxx+1):
    for y in range(miny, maxy+1):
        for z in range(minz, maxz+1):
            toCheck = (x, y, z)
            if not toCheck in cubes and not toCheck in interior and not toCheck in exterior:
                (isExterior, toAdd) = updateSets(toCheck, cubes)
                if isExterior:
                    exterior = exterior.union(toAdd)
                else:
                    interior = interior.union(toAdd)

totalWithoutInternal = 0
for cube in cubes:
    for look in lookDirs:
        if not (cube[0] + look[0], cube[1] + look[1], cube[2] + look[2]) in cubes and not (cube[0] + look[0], cube[1] + look[1], cube[2] + look[2]) in interior:
            totalWithoutInternal += 1

print(totalWithoutInternal)