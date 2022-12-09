class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.directories = {}

    def AddFile(self, name, size):
        self.files.append((name, size))

    def AddDirectory(self, name):
        self.directories[name] = Directory(name, self)

    def GetSumOfFileSizes(self):
        sum = 0
        for f in self.files:
            sum += int(f[1])
        return sum

    def GetTotalSize_PartOne(self, maxSize, sizes):
        fileSum = self.GetSumOfFileSizes()
        
        for dir in self.directories.values():
            fileSum += dir.GetTotalSize_PartOne(maxSize, sizes)

        if fileSum <= maxSize:
            sizes.append(fileSum)

        return fileSum

    def GetTotalSize_PartTwo(self, minSize, sizes):
        fileSum = self.GetSumOfFileSizes()
        
        for dir in self.directories.values():
            fileSum += dir.GetTotalSize_PartTwo(minSize, sizes)

        if fileSum >= minSize:
            sizes.append(fileSum)

        return fileSum

    def Print(self, indent):
        whiteSpace = ""
        for i in range(indent):
            whiteSpace += " "
        
        print(f"{whiteSpace}-{self.name}")
        for f in self.files:
            print(f"{whiteSpace}{f}")
        for dir in self.directories.values():
            dir.Print(indent + 2)


data = open("data/Day7Data.txt", 'r').readlines()
totalMemory = 70000000
requiredMemory = 30000000

root = Directory("/", None)
activeDir = root

for d in data:
    dat = d.strip()
    if dat[0] == "$":
        if dat[:4] == "$ cd":
            if dat == "$ cd /":
                activeDir = root
            elif dat == "$ cd ..":
                activeDir = activeDir.parent
            else:
                dirName = dat[len("$ cd "):]
                if not dirName in activeDir.directories.keys():
                    activeDir.AddDirectory(dirName)
                activeDir = activeDir.directories[dirName]
        elif dat[:4] == "$ ls":
            i = 0 # This is kinda useless
        else:
            raise Exception("This should never happen")
    else:
        if dat[:len("dir ")] == "dir ":
            activeDir.AddDirectory(dat[len("dir "):])
        else:
            [size, fname] = dat.split()
            activeDir.AddFile(fname, size)

#root.Print(0)
sizes = []
rootSize = root.GetTotalSize_PartOne(100000, sizes)
print(sum(sizes))

sizes = []
memToFree = requiredMemory - (totalMemory - rootSize)
rootSize = root.GetTotalSize_PartTwo(memToFree, sizes)
print(min(sizes))
