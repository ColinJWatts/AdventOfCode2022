get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

data = get_input("data/Day19Data.txt")
#numMin = 24
numMin = 32

class RobotFactory:
    def __init__(self, id, o_ocost, c_ocost, ob_ocost, ob_ccost, g_ocost, g_obcost):
        self.id = id
        self.oreRobotOreCost = o_ocost
        self.clayRobotOreCost = c_ocost
        self.obsidianRobotOreCost = ob_ocost
        self.obsidianRobotClayCost = ob_ccost
        self.geodeRobotOreCost = g_ocost
        self.geodeRobotObsidianCost = g_obcost

        self.allowOre = True
        self.allowClay = True
        self.allowObsidian = True

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.oreRobots = 1
        self.clayRobots = 0
        self.obsidianRobots = 0
        self.geodeRobots = 0

        self.history = []

    def GetRobotCounts(self):
        return (self.oreRobots, self.clayRobots, self.obsidianRobots, self.geodeRobots)

    def GetMaxOreCost(self):
        return max([self.oreRobotOreCost, self.clayRobotOreCost, self.obsidianRobotOreCost, self.geodeRobotOreCost])

    def GetResourceCounts(self):
        return (self.ore, self.clay, self.obsidian, self.geodes)

    def Copy(self):
        newFactory = RobotFactory(self.id, self.oreRobotOreCost, self.clayRobotOreCost, self.obsidianRobotOreCost, self.obsidianRobotClayCost, self.geodeRobotOreCost, self.geodeRobotObsidianCost)
        newFactory.ore = self.ore
        newFactory.clay = self.clay
        newFactory.obsidian = self.obsidian
        newFactory.geodes = self.geodes

        newFactory.oreRobots = self.oreRobots
        newFactory.clayRobots = self.clayRobots
        newFactory.obsidianRobots = self.obsidianRobots
        newFactory.geodeRobots = self.geodeRobots

        newFactory.allowOre = self.allowOre
        newFactory.allowClay = self.allowClay
        newFactory.allowObsidian = self.allowObsidian

        newFactory.history = self.history.copy()

        return newFactory

    def TakeAction(self, action, actions, minute):
        histToAdd = f"== Minute {minute+1} ==\n"
        self.ore += self.oreRobots
        self.clay += self.clayRobots
        self.obsidian += self.obsidianRobots
        self.geodes += self.geodeRobots

        robotBuilt = False

        if action == "ore":
            self.oreRobots += 1
            self.ore = self.ore - self.oreRobotOreCost
            histToAdd += f"Spend {self.oreRobotOreCost} ore to start building a ore-collecting robot.\n"
            self.allowOre = True
            self.allowClay = True
            self.allowObsidian = True
            robotBuilt = True
        elif "ore" in actions:
            self.allowOre = False
        if action == "clay":
            self.clayRobots += 1
            self.ore = self.ore - self.clayRobotOreCost
            histToAdd += f"Spend {self.clayRobotOreCost} ore to start building a clay-collecting robot.\n"
            self.allowOre = True
            self.allowClay = True
            self.allowObsidian = True
            robotBuilt = True
        elif "clay" in actions and not robotBuilt:
            self.allowClay = False
        if action == "obsidian":
            self.obsidianRobots += 1
            self.ore = self.ore - self.obsidianRobotOreCost
            self.clay = self.clay - self.obsidianRobotClayCost
            histToAdd += f"Spend {self.obsidianRobotOreCost} ore and {self.obsidianRobotClayCost} clay to start building an obsidian-collecting robot.\n"
            self.allowOre = True
            self.allowClay = True
            self.allowObsidian = True
        elif "obsidian" in actions and not robotBuilt:
            self.allowObsidian = False
        if action == "geode":
            self.geodeRobots += 1
            self.ore = self.ore - self.geodeRobotOreCost
            self.obsidian = self.obsidian - self.geodeRobotObsidianCost
            histToAdd += f"Spend {self.geodeRobotOreCost} ore and {self.geodeRobotObsidianCost} obsidian to start building a geode-collecting robot.\n"

        histToAdd += f"{self.oreRobots} ore-collecting robots; you now have {self.ore} ore.\n"
        histToAdd += f"{self.clayRobots} clay-collecting robots; you now have {self.clay} clay.\n"
        histToAdd += f"{self.obsidianRobots} obsidian-collecting robots; you now have {self.obsidian} obsidian.\n"
        histToAdd += f"{self.geodeRobots} geode-collecting robots; you now have {self.geodes} geodes.\n"
        self.history.append(histToAdd)

    def GetPossibleActions(self):
        actions = ["none"]
        if self.ore >= self.oreRobotOreCost and self.GetMaxOreCost() > self.oreRobots and self.allowOre:
            actions.append("ore")
        if self.ore >= self.clayRobotOreCost and self.obsidianRobotClayCost > self.clayRobots and self.allowClay:
            actions.append("clay")
        if self.ore >= self.obsidianRobotOreCost and self.clay >= self.obsidianRobotClayCost and self.geodeRobotObsidianCost > self.obsidianRobots and self.allowObsidian:
            actions.append("obsidian")
        if self.ore >= self.geodeRobotOreCost and self.obsidian >= self.geodeRobotObsidianCost:
            #if we CAN make a geode robot we should
            actions.append("geode")
            #actions = ["geode"]

        return actions

factories = []

for d in data:
    print (d)
    [blueprint, robotOreCosts] = d.split(":")
    bluePrintId = int(blueprint.split(" ")[1])
    oreRobotOreCost = int(robotOreCosts.split(".")[0].strip()[len("Each ore robot costs "):].split(" ")[0])
    clayRobotOreCost = int(robotOreCosts.split(".")[1].strip()[len("Each clay robot costs "):].split(" ")[0])
    obsidianRobotOreCost = int(robotOreCosts.split(".")[2].strip()[len("Each obsidian robot costs "):].split(" ")[0])
    obsidianRobotClayCost = int(robotOreCosts.split(".")[2].strip()[len("Each obsidian robot costs "):].split(" ")[3])
    geodeRobotOreCost = int(robotOreCosts.split(".")[3].strip()[len("Each geode robot costs "):].split(" ")[0])
    geodeRobotObsidianCost = int(robotOreCosts.split(".")[3].strip()[len("Each geode robot costs "):].split(" ")[3])
    factories.append(RobotFactory(bluePrintId, oreRobotOreCost, clayRobotOreCost, obsidianRobotOreCost, obsidianRobotClayCost, geodeRobotOreCost, geodeRobotObsidianCost))

factories = factories[:3]
totalQuality = 0
for factory in factories:
    maxGeodes = 0
    maxfactory = factory
    toCheck = [factory]

    test = dict()

    for minute in range(numMin):
        next = []
        print(f"minute {minute} has {len(toCheck)} paths")

        maxExtraGeodes = sum([i for i in range(numMin-minute+1)])   
        # print(maxExtraGeodes)   
        prevMaxes = tempMax
        tempMax = maxGeodes
        for f in toCheck:
            actions = f.GetPossibleActions()
            
            for a in actions:
                
                # if a == "geode" and f.geodes + maxExtraGeodes < maxGeodes:
                #     continue
                # elif f.geodes + maxExtraGeodes - (numMin - minute) < maxGeodes:
                #     continue

                fcopy = f.Copy()
                fcopy.TakeAction(a, actions, minute)

                robotCounts = fcopy.GetRobotCounts()
                resourceCounts = fcopy.GetResourceCounts()
                if not robotCounts in test.keys():
                    test[robotCounts] = resourceCounts
                else: 
                    if resourceCounts[0] <= test[robotCounts][0] and resourceCounts[1] <= test[robotCounts][1] and resourceCounts[2] <= test[robotCounts][2] and resourceCounts[3] <= test[robotCounts][3]:
                        continue
                
                if fcopy.geodes < maxGeodes:
                    continue

                if fcopy.geodes > maxGeodes and fcopy.geodes > tempMax:
                    tempMax = fcopy.geodes
                    maxfactory = fcopy
                next.append(fcopy)
        maxGeodes = tempMax
        toCheck = next

    totalQuality += factory.id * maxGeodes
    print(f"factory {factory.id} produced {maxGeodes} geodes for quality {factory.id * maxGeodes}")

print(totalQuality)