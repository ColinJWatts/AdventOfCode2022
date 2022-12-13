get_input = lambda filename: [l.strip('\n') for l in open(filename,'r+',encoding='utf-8').readlines()]

def cons(a, b):
    return (a, b)

def car(a):
    if a is None:
        return None
    resp = a[0]
    return resp

def cdr(a):
    if a is None:
        return None
    resp = a[1]
    return resp

def PrintCarList(a):
    if a is None:
        return ']'
    val = car(a)
    resp = ""
    if isinstance(val, int):
        resp += str(val)
        if not cdr(a) is None:
            resp += ","
    else:
        resp+="["
        resp += PrintCarList(val)
    return resp + PrintCarList(cdr(a))

def FindSublist(raw):
    # we know the first element should be a '[' so just skip that one
    openBrackets = 1
    iter = 1
    sublist = "["

    while openBrackets > 0:
        if raw[iter] == '[':
            openBrackets += 1
        elif raw[iter] == ']':
            openBrackets -= 1
        
        sublist += raw[iter]
        iter += 1

    return sublist

def FindNextValue(raw):
    # this gets the next integer value (the next value should be an int)
    vals = raw.split(',')
    return vals[0]

def ParsePacket(raw):
    if raw == "[]":
        return(None, None)
    raw = raw[1:len(raw) - 1] # get rid of square brackets

    vals = []
    
    while raw:
        if raw[0] == '[':
            sublist = FindSublist(raw)
            vals.append(ParsePacket(sublist))
            raw = raw[len(sublist):]
        elif raw[0] == ',':
            raw = raw[1:]
        else:
            val = FindNextValue(raw)
            raw = raw[len(val):]
            vals.append(int(val))

    resp = None
    for i in range(len(vals) - 1, -1, -1):
        resp = cons(vals[i], resp)

    return resp

def ArePacketsInOrder(packetSet):
    [first, second] = packetSet
    firstVal = car(first)
    secondVal = car(second)

    # left list ran out first
    if firstVal is None and not secondVal is None:
        print("Left list ran out first, packets are in order")
        return True
    
    # right list ran out first
    if not firstVal is None and secondVal is None:
        print("Right list ran out first, packets are NOT in order")
        return False

    # if both are none, return none and continue
    if firstVal is None and secondVal is None:
        return None

    # check if we're comparing integers
    if isinstance(firstVal, int) and isinstance(secondVal, int):
        if firstVal < secondVal:
            print(f"Left value ({firstVal}) is smaller than Right Value ({secondVal}). Packets are in order")
            return True
        if secondVal < firstVal:
            print(f"Right value ({secondVal}) is smaller than Left Value ({firstVal}). Packets are NOT in order")
            return False
    else:
        # at this point at least one of our inputs is a list
        if isinstance(firstVal, int):
            firstVal = cons(firstVal, None)

        if isinstance(secondVal, int):
            secondVal = cons(secondVal, None)

        temp = ArePacketsInOrder([firstVal, secondVal])
        # if sublists determine if packets are in order, return that
        if not temp is None:
            return temp

    # otherwise, try on the remainder of the list
    return ArePacketsInOrder([cdr(first), cdr(second)])

data = get_input("data/Day13Data.txt")

packets = []
packetList = []

curr = []
for d in data:
    if d != "":
        p = ParsePacket(d)
        curr.append(p)
        packetList.append(p)
    else:
        packets.append(curr)
        curr = []

packets.append(curr)

total = 0
i = 1

for p in packets:
    print(f"PacketNumber: {i}")
    val =  ArePacketsInOrder(p)
    if val is None: # if both packets are the same
        total = total
    elif val:
        total += i

    i += 1
    print("")

print(f"Total: {total}")

packetList.append(ParsePacket("[[2]]"))
packetList.append(ParsePacket("[[6]]"))

#lol bubble sort
for i in range(len(packetList)):
    for j in range(len(packetList)-1):
        if not ArePacketsInOrder([packetList[j], packetList[j+1]]):
            temp = packetList[j]
            packetList[j] = packetList[j+1]
            packetList[j+1] = temp

for i in range(len(packetList)):
    print(i+1)
    print('[' + PrintCarList(packetList[i]))
    print("")