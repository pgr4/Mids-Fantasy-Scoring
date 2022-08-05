import http_requests
from maths import getRBRating, getWRRating
import sys
import constants
from os import walk

year = 2021
seasonType = "REG"
teamIds = []
mainPath = "C:\\Users\\iampg\\"
teamPath = f"{mainPath}teams\\"
playerPath = f"{mainPath}players\\"
rbsPath = f"{playerPath}rbs\\"
wrsPath = f"{playerPath}wrs\\"

def getHierarchyFilePath():
    return f"{mainPath}\\hierarchy.json"

def getRosterFilePath(teamId):
    return f"{teamPath}\\${teamId}.json"

def getRBFilePath(playerId):
    return f"{rbsPath}\\{playerId}.json"

def getWRFilePath(playerId):
    return f"{wrsPath}\\{playerId}.json"

def writeToFile(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()
    
def getFilenamesInDir(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    return f

def sortTuples(list):
    return(sorted(list, key = lambda x: x[2])) 

def getHierarchy():
    return http_requests.getLeagueHierarchy()

def getRoster(teamId):
    return http_requests.getTeamRoster(teamId)

def getPlayer(playerId):
    return http_requests.getPlayerProfile(playerId)

def usePlayer(player):
    if player.position == "RB":
        if constants.rbs.__contains__(player.name):
            return True
        else:
            print(f"Ignoring {player.name}")
    if player.position == "WR":
        if constants.wrs.__contains__(player.name):
            return True
        else:
            print(f"Ignoring {player.name}")
            
    return False

def getDataThroughApi():
    # Get League
    lh = getHierarchy()
    teams = []
    rbs = []
    wrs = []
    
    # Obtain all of the team ids in the entire league
    for conference in lh.conferences:
        for division in conference.divisions:
            for team in division.teams:
                teamIds.append(team.id)
                teams.append(team)

    # Loop Through TeamIds
    for teamId in teamIds:
        # Get Team Roster
        tr = getRoster(teamId)
        teams.append(tr)
        # Loop Through Roster/Players
        for player in tr.players:
            # We only care about WR/RB/QB no scrubs here
            if usePlayer(player): 
                # Get the player's profile
                pp = getPlayer(player.id)
                # Loop through the players seasons and get the one you care about 
                for season in pp.seasons:
                    # We only care about a single years stats
                    if season.year == year and season.name == seasonType:
                        if player.position == "RB":
                            rbs.append(pp)
                        elif player.position == "WR":
                            wrs.append(pp)
    
    return (lh, teams, rbs, wrs)

def getDataThroughFiles():
    # Get League
    lh = open(getHierarchyFilePath())
    teams = []
    for filename in getFilenamesInDir(teamPath):
        teams.append(open(filename))
    rbs = []
    for filename in getFilenamesInDir(rbsPath):
        rbs.append(open(filename))
    wrs = []
    for filename in getFilenamesInDir(wrsPath):
        wrs.append(open(filename))
        
    return (lh, teams, rbs, wrs)
                       

def showScores(players):
    scores = []
    # Loop through the players seasons and get the one you care about 
    for season in pp.seasons:
        # We only care about a single years stats
        if season.year == year and season.name == seasonType:
            if player.position == "RB":
                # Use the Current Player's team in order to get the 
                rating = getRBRating(season.teams[0].statistics, tr.alias)
            elif player.position == "WR":
                rating = getWRRating(season.teams[0].statistics, tr.alias)
            else:
                pass
    
    # Add (Name, Position, Score) to list
    scores.append((player.name, player.position, rating))
    
    # Sort the scores
    scores = sortTuples(scores)

    # Print RBs sorted by Rating
    print('-------Running Backs-------')
    for score in scores:
        if score[1] == "RB":
            print(f"{score[0]} - {score[2]}")
            
    # Print WRs sorted by Rating
    print('-------Wide Receivers-------')
    for score in scores:
        if score[1] == "WR":
            print(f"{score[0]} - {score[2]}")

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])

print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")

match sys.argv[0]:
        case "download":
            h, r, rbs, wrs = getDataThroughApi()
            writeToFile(getHierarchyFilePath(), h)
            writeToFile(getRosterFilePath(), r)
            for rb in rbs:
                writeToFile(getRBFilePath(rb.name), rb)
            for wr in wrs:
                writeToFile(getWRFilePath(wr.name), wr)
            pass
        case "run":
            h, r, rbs, wrs = getDataThroughFiles()
            pass