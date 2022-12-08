from SortedBuffer import SortedBuffer

data = open("Day1Data.txt", 'r').readlines()

currElfNum = 1
currElfVal = 0

#part 2
topThree = SortedBuffer(3)

for i in range(len(data)):
    if data[i].strip() != "":
        data[i] = int(data[i].strip())
        currElfVal += data[i]
    else: 
        data[i] = ""
        topThree.AddVal(currElfVal, currElfNum)

        currElfNum += 1
        currElfVal = 0


sum = 0
for i in range(len(topThree.buffer)):
    print(f"Elves: {topThree.keys[i]}   Val: {topThree.buffer[i]}")
    sum += topThree.buffer[i]

print(f"Sum : {sum}")



