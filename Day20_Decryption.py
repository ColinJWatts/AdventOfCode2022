get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

class Point:
    def __init__(self, val):
        self.value = val

data = [int(d) for d in get_input("data/Day20Data.txt")]
moveOrder = []
values = []
zeroPoint = None
dkey = 811589153

for i in range(len(data)):
    pointer = Point(data[i] * dkey)
    if data[i] == 0:
        zeroPoint = pointer
    values.append(pointer)
    moveOrder.append(pointer)

for j in range(10):
    for i in range(len(moveOrder)):
        pointer = moveOrder[i]
        idx = values.index(pointer)
        values.pop(idx)
        newIdx = (pointer.value + idx) % len(values)
        if not newIdx == 0:
            values.insert(newIdx, pointer)
        else:
            values.append(pointer)

zeroIdx = values.index(zeroPoint)
print(f"1000th: {values[(1000+zeroIdx)%len(values)].value}\n2000th: {values[(2000+zeroIdx)%len(values)].value}\n3000th: {values[(3000+zeroIdx)%len(values)].value}")
print(values[(1000+zeroIdx)%len(values)].value + values[(2000+zeroIdx)%len(values)].value + values[(3000+zeroIdx)%len(values)].value)