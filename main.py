import http_requests
from maths import getRBRating, getWRRating
import sys
from constants import full_list
from os import walk, mkdir, path
import json
import datetime

year = 2021
seasonType = "REG"
teamIds = []
mainPath = "C:\\Users\\iampg\\Midtasy\\"
playerPath = f"{mainPath}players\\"
rbsPath = f"{playerPath}rbs\\"
wrsPath = f"{playerPath}wrs\\"

def createDir(dir):
    if doesFileExist(dir) == False:
        mkdir(dir)

def createFolders():
    createDir(mainPath)
    createDir(playerPath)
    createDir(rbsPath)
    createDir(wrsPath)

def getHierarchyFilePath():
    return f"{mainPath}\\hierarchy.json"

def getRosterFilePath():
    return f"{mainPath}\\teams.json"

def getRBFilePath(playerId):
    return f"{rbsPath}\\{playerId}.json"

def getWRFilePath(playerId):
    return f"{wrsPath}\\{playerId}.json"

def doesFileExist(filePath):
    return path.exists(filePath)

def writeToObjectFile(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()
    
def writeToArrayFile(path, array):
    f = open(path, "w")
    f.write("[")
    f.close()
    
    f = open(path, "a")
    first = True
    for data in array:
        if first == False: 
            f.write(",")
        else:
            first = False
        f.write(data)
        
    f.write("]")
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
        if full_list.__contains__(player.name) and doesFileExist(rbsPath + player.name) == False:
            return True
        else:
            print(f"Ignoring {player.name}")
    if player.position == "WR":
        if full_list.__contains__(player.name) and doesFileExist(wrsPath + player.name) == False:
            return True
        else:
            print(f"Ignoring {player.name}")
            
    return False

def getDataThroughApi():
    # Get League
    lh = getHierarchy()
    lh_obj = http_requests.convertToObject(lh)
    
    teams = []
    rbs = []
    wrs = []
    
    # Obtain all of the team ids in the entire league
    for conference in lh_obj.conferences:
        for division in conference.divisions:
            for team in division.teams:
                teamIds.append(team.id)

    # Loop Through TeamIds
    for teamId in teamIds:
        # Get Team Roster
        tr = getRoster(teamId)
        tr_obj = http_requests.convertToObject(tr)
        teams.append(http_requests.convertToString(tr))
        # Loop Through Roster/Players
        for player in tr_obj.players:
            # We only care about WR/RB/QB no scrubs here and ones we don't have a file for already
            if usePlayer(player): 
                # Get the player's profile
                pp = getPlayer(player.id)
                pp_obj = http_requests.convertToObject(pp)
                # Loop through the players seasons and get the one you care about 
                for season in pp_obj.seasons:
                    # We only care about a single years stats
                    if season.year == year and season.name == seasonType:
                        if player.position == "RB":
                            rbs.append((player.name, http_requests.convertToString(pp)))
                        elif player.position == "WR":
                            wrs.append((player.name, http_requests.convertToString(pp)))
    
    return (http_requests.convertToString(lh),
            teams, 
            rbs,
            wrs)

def getDataThroughFiles():
    # Get League
    ## TODO: ...
    lh = {} ## open(getHierarchyFilePath())
    teams = []
    # TODO: THIS CHANGED TO A SINGLE FILE
    # for filename in getRosterFilePath():
    #     teams.append(open(filename))
    rbs = []
    for filename in getFilenamesInDir(rbsPath):
        with open(rbsPath + filename) as file:
            rbs.append(json.load(file))
    wrs = []
    for filename in getFilenamesInDir(wrsPath):
        with open(wrsPath + filename) as file:
            wrs.append(json.load(file))
        
    return (lh, teams, rbs, wrs)

def sortScores(scores):
    return sortTuples(scores)

def outputScores(header, scores):
    # Sort the scores
    scores = sortScores(scores)
    
    # Print RBs sorted by Rating
    print('header')
    for score in scores:
        if score[1] == "RB":
            print(f"{score[0]} - {score[2]}")
            
    # Print WRs sorted by Rating
    print('')
    for score in scores:
        if score[1] == "WR":
            print(f"{score[0]} - {score[2]}")           

def showScores(players):
    scores = []
    for player in players:
        # Loop through the players seasons and get the one you care about 
        for season in player['seasons']:
            # We only care about a single years stats
            if season['year'] == year and season['name'] == seasonType:
                # Only go through the scores if the player was good enough to play
                if season['teams'][0]['statistics']['games_played'] != 0:
                    if player['position'] == "RB":
                        # Use the Current Player's team in order to get the 
                        scores.append((player['name'], player['position'], getRBRating(season['teams'][0]['statistics'], season['teams'][0]['alias'])))
                    elif player['position'] == "WR":
                        # Add (Name, Position, Score) to list
                        scores.append((player['name'], player['position'], getWRRating(season['teams'][0]['statistics'], season['teams'][0]['alias'])))
                    else:
                        pass
    
    outputScores(scores)

# MAIN    

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])

print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")

match sys.argv[1]:
        case "--download":
            createFolders()
            
            tuple = getDataThroughApi()
            lh = tuple[0]
            teams = tuple[1]
            rbs = tuple[2]
            wrs = tuple[3]
            
            writeToObjectFile(getHierarchyFilePath(), lh)
            writeToArrayFile(getRosterFilePath(), teams)
            for rbTuple in rbs:
                writeToObjectFile(getRBFilePath(rbTuple[0]), rbTuple[1])
            for wrTuple in wrs:
                writeToObjectFile(getWRFilePath(wrTuple[0]), wrTuple[1])
            pass
        case "--run":
            lh, teams, rbs, wrs = getDataThroughFiles()
            showScores('-------Running Backs -------', rbs)
            showScores('-------Wide Receivers-------', wrs)
            pass