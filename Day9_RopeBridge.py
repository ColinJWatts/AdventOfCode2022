
def IsHeadOutOfRange(head, tail):
    acceptableLocs = []

    x = -1
    while x <= 1: 
        y = -1
        while y <= 1:
            acceptableLocs.append((tail[0] + x, tail[1] + y))
            y += 1
        x += 1
    
    return not head in acceptableLocs

# this function is some jank. I do not like this
def GetNewTailLocation(head, tail):
    if head[0] == tail[0]:
        # x is the same
        if head[1] > tail[1]:
            return (tail[0], tail[1] + 1)
        else:
            return (tail[0], tail[1] - 1)
    elif head[1] == tail[1]:
        # y is the same
        if head[0] > tail[0]:
            return (tail[0] + 1, tail[1])
        else:
            return (tail[0] - 1, tail[1])
    elif head[0] > tail[0] and head[1] > tail[1]:
        return (tail[0] + 1, tail[1] + 1)
    elif head[0] > tail[0] and head[1] < tail[1]:
        return (tail[0] + 1, tail[1] - 1)
    elif head[0] < tail[0] and head[1] > tail[1]:
        return (tail[0] - 1, tail[1] + 1)
    elif head[0] < tail[0] and head[1] < tail[1]:
        return (tail[0] - 1, tail[1] - 1)
    else:
        raise Exception("something went wrong")

data = open("data/Day9Data.txt", 'r').readlines()

startingPos = (0,0)
numKnots = 10
knots = [startingPos for i in range(numKnots)]

directionMap = {
    'U' : (0, -1),
    'D' : (0, 1),
    'L' : (-1, 0),
    'R' : (1, 0)
}    

tailLocations = [knots[-1]]

for d in data:
    dat = d.strip()
    [direction, distance] = dat.split(" ")
    distance = int(distance)

    unitMove = directionMap[direction]

    for i in range(distance):
        knots[0] = (knots[0][0] + unitMove[0], knots[0][1] + unitMove[1])

        for i in range(numKnots - 1):

            if IsHeadOutOfRange(knots[i], knots[i+1]):
                #we need to move knot[i+1]
                knots[i+1] = GetNewTailLocation(knots[i], knots[i+1])   
                
        if not knots[-1] in tailLocations:
            tailLocations.append(knots[-1])

print(f"Tail visited {len(tailLocations)} locations")