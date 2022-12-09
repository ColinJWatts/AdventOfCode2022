
#part 1
def StandardizeMatchup(matchup):
    # this takes in a matchup and standardizes to to [R, P, S]
    opponentLookup = {
        'A' : 'R',
        'B' : 'P',
        'C' : 'S'
    } 

    playerLookup = {
        'X' : 'R',
        'Y' : 'P',
        'Z' : 'S'
    }
        
    return [opponentLookup[matchup[0]], playerLookup[matchup[1]]]


#part 2 
def StandardizeMatchups2(matchup):
    opponentLookup = {
        'A' : 'R',
        'B' : 'P',
        'C' : 'S'
    } 

    playerLookup = {
        ('R', 'X') : 'S',
        ('R', 'Y') : 'R',
        ('R', 'Z') : 'P',
        ('P', 'X') : 'R',
        ('P', 'Y') : 'P',
        ('P', 'Z') : 'S',
        ('S', 'X') : 'P',
        ('S', 'Y') : 'S',
        ('S', 'Z') : 'R'
    }

    oppenentThrow = opponentLookup[matchup[0]]
    playerThrow = playerLookup[(oppenentThrow, matchup[1])]
    return[oppenentThrow, playerThrow]


def GetOutcomeScore(matchup):
    if (matchup[0] == matchup[1]):
        return 3

    winningMatchups = [['R', 'P'], ['P', 'S'], ['S', 'R']]
    if matchup in winningMatchups:
        return 6
    
    return 0


playScoreLookup = {
    'R' : 1,
    'P' : 2,
    'S' : 3
}

data = open("data/Day2Data.txt", 'r').readlines()

matchups = []
totalScore = 0
for d in data:
    temp = d.strip().split(" ")
    print(temp)
    temp = StandardizeMatchups2(temp)
    matchups.append(temp)
    roundScore = playScoreLookup[temp[1]] + GetOutcomeScore(temp)
    print(f"Opponent threw: {temp[0]}   I threw {temp[1]}")
    print(f"Score: {playScoreLookup[temp[1]]} + {GetOutcomeScore(temp)} = {roundScore}")
    totalScore += roundScore

print(f"Total Score: {totalScore}")

