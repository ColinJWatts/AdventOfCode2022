def AreBufferCharactersAllDifferent(buffer):
    lookup = {}
    for val in buffer:
        if not val in lookup.keys():
            lookup[val] = 1
        else:
            return False

    return True

data = open("data/Day6Data.txt", 'r').read()

buffer = []
maxBufferSize = 4

charCount = 0

for i in range(len(data)):
    charCount += 1

    print(data[i])

    buffer.append(data[i])
    if len(buffer) > maxBufferSize:
        buffer.pop(0)
    
        if AreBufferCharactersAllDifferent(buffer):
            break

print(charCount)

