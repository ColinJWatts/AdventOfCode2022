class SortedBuffer:
    def __init__(self, maxLen):
        self.maxLen = maxLen
        self.buffer = []
        self.keys = []

    def AddVal(self, val, key):        
        for i in range(len(self.buffer)):
            if val == self.buffer[i]:
                self.keys[i].append(key)
                return
            elif val > self.buffer[i]:
                self.buffer.insert(i, val)
                self.keys.insert(i, [key])
                if len(self.buffer) > self.maxLen:
                    self.buffer = self.buffer[:self.maxLen]
                    self.keys = self.keys[:self.maxLen]
                return
        
        if len(self.buffer) < self.maxLen:
            self.buffer.append(val)
            self.keys.append([key])

data = open("data/Day1Data.txt", 'r').readlines()

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