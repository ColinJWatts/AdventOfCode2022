get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day10Data.txt")
registerVal = 1
cycle = 0
valPerCycle = []

for d in data: 
    if d == "noop":
        cycle += 1
        valPerCycle.append(registerVal)
    elif d[:len("addx")] == "addx":
        cycle += 2
        valPerCycle += [registerVal, registerVal]
        registerVal += int(d.split(" ")[1])

totalSignal = 0
for i in range(19, len(valPerCycle), 40):
    totalSignal += (i+1) * valPerCycle[i]

print(f"Total Signal: {totalSignal}")

crt = ""

for i in range(len(valPerCycle)):
    pixelPos = i % 40
    if pixelPos == 0:
        crt += "\n"
    
    if valPerCycle[i] == pixelPos or valPerCycle[i] + 1 == pixelPos or valPerCycle[i] - 1 == pixelPos:
        crt += "#"
    else:
        crt += "."

print(crt)