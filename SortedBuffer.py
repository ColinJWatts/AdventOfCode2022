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