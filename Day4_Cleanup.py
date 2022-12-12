def GetAssignmentAsTuple(raw):
    temp = raw.split("-")
    return (int(temp[0]), int(temp[1]))

def IsAInB(a, b):
    return a[0] >= b[0] and a[1] <= b[1]

def DoAandBOverlap(a, b):
    overlap = list(range(max(a[0], b[0]), min(a[1], b[1]) + 1))

    return len(overlap) > 0

data = open("data/Day4Data.txt", 'r').readlines()

totalContained = 0
totalOverlapping = 0

for d in data:
    temp = d.strip().split(",")
    elf1Assignment = GetAssignmentAsTuple(temp[0])
    elf2Assignment = GetAssignmentAsTuple(temp[1])

    if IsAInB(elf1Assignment, elf2Assignment) or IsAInB(elf2Assignment, elf1Assignment):
        totalContained += 1

    if DoAandBOverlap(elf1Assignment, elf2Assignment):
        totalOverlapping += 1
    else: 
        print(f"{elf1Assignment}, {elf2Assignment}")

print(totalContained)
print(totalOverlapping)