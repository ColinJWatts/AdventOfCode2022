get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day15Data.txt")

def ManhattenDist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def ParseSenorAndBeacon(raw):
    raw = raw.replace("Sensor at x=", "")
    raw = raw.replace("closest beacon is at x=", "")
    sensorDat, beaconDat = raw.split(":")
    sensorDat = sensorDat.replace("y=", "").split(",")
    beaconDat = beaconDat.replace("y=", "").split(",")
    sensorLoc = (int(sensorDat[0]), int(sensorDat[1]))
    beaconLoc = (int(beaconDat[0]), int(beaconDat[1]))
    dist =  ManhattenDist(sensorLoc, beaconLoc)
    
    return (sensorLoc, beaconLoc, dist)

def MergeSpace(spaces):
    result = []
    if len(spaces) == 0:
        return result
    curr = (spaces[0])
    for i in range(1, len(spaces)):
        if spaces[i][0] <= curr[1]:
            #merge the spaces
            if spaces[i][1] > curr[1]:
                curr = (curr[0], spaces[i][1])
        else:
            result.append(curr)
            curr = spaces[i]
    result.append(curr)
    return result


(maxX, maxY, minX, minY) = (-100000000, -100000000, 100000000, 100000000)

sensors = []
beacons = []
distances = []

for d in data:
    (sensorPos, beaconPos, dist) = ParseSenorAndBeacon(d)
    sensors.append(sensorPos)
    beacons.append(beaconPos)
    distances.append(dist)

    if sensorPos[0] + dist > maxX:
        maxX = sensorPos[0] + dist
    if sensorPos[1] + dist > maxY:
        maxY = sensorPos[1] + dist
    if sensorPos[0] - dist < minX:
        minX = sensorPos[0] - dist
    if sensorPos[1] - dist < minY:
        minY = sensorPos[1] - dist

for lookPos in range(0, 4000000):
    totalSeen = 0

    projViews = []
    for i in range(len(sensors)):
        projDist = distances[i] - abs(sensors[i][1] - lookPos)
        if projDist >= 0:
            low = sensors[i][0] - projDist
            hi = sensors[i][0] + projDist
            projViews.append((low, hi))

    projViews = sorted(projViews, key=lambda x: x[0])

    merged = MergeSpace(projViews)

    if len(merged) > 1:
        print(f"{lookPos}: {merged}")

# for i in range(minX-1, maxX+1):
#     for j in range(len(sensors)):
#         testPos = (i, lookPos)
#         if not testPos in sensors and not testPos in beacons and ManhattenDist(sensors[j], testPos) <= distances[j]:
#             totalSeen += 1
#             break

# print(totalSeen)
