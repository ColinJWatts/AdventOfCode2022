def ConstructLookup(raw):
    resp = {}
    for c in raw:
        if c in resp.keys():
            resp[c] += 1
        else:
            resp[c] = 1

    return resp

def GetItemPriority(item):
    if item.isupper():
        return ord(item) - ord('A') + 27
    else:
        return ord(item) - ord('a') + 1

class RuckSack:
    def __init__(self, raw):
        self.raw = raw
        split = int(len(raw)/2)
        self.full = ConstructLookup(raw)
        self.left = ConstructLookup(raw[:split])
        self.right = ConstructLookup(raw[split:])

    def GetCommonItem(self):
        for i in self.left.keys():
            if i in self.right.keys():
                return i

    def GetGroupBadge(self, other1, other2):
        firstPass = []
        for k in self.full.keys():
            if k in other1.full.keys():
                firstPass.append(k)

        for k in firstPass:
            if k in other2.full.keys():
                return k


data = open("data/Day3Data.txt", 'r').readlines()
ruckSacks = []
totalPriority = 0

groupCount = 0
totalBadgePriority = 0

for d in data:
    print(d.strip())
    ruckSacks.append(RuckSack(d.strip()))
    item = ruckSacks[-1].GetCommonItem()
    priority = GetItemPriority(item)
    totalPriority += priority

    #part 2
    if groupCount == 2: 
        # the last three ruckSacks make up a group
        badge = ruckSacks[-3].GetGroupBadge(ruckSacks[-2], ruckSacks[-1])
        totalBadgePriority += GetItemPriority(badge)

    groupCount = (groupCount + 1) % 3

print(f"Total Priority: {totalPriority}")
print(f"Total Badge Priority: {totalBadgePriority}")