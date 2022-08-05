from re import X
import string
import tracemalloc
import requests
import json
from types import SimpleNamespace
from time import sleep

baseUrl = "http://api.sportradar.us/"
apiKey = "f78x2ss9h2zn2cqrntn949gk"
languageCode = "en"
version = "v7"
# Throttle 1 sec / 1000 per 30 days

def printResponse(response: requests.Response):
    ## print(response.url)
    ## print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
    pass

def convertToObject(response: requests.Response):
    return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

def makeGetRequest(url):
    satisfyQPS()
    response = requests.get(url)
    printResponse(response)
    return response

def satisfyQPS():
    sleep(1.5)

def getPlayerProfile(playerId):
    fullUrl = baseUrl + f"nfl/official/trial/{version}/{languageCode}/players/{playerId}/profile.json?api_key={apiKey}"
    
    return convertToObject(makeGetRequest(fullUrl))

def getTeamRoster(teamId):
    fullUrl = baseUrl + f"nfl/official/trial/{version}/{languageCode}/teams/{teamId}/full_roster.json?api_key={apiKey}"
    
    return convertToObject(makeGetRequest(fullUrl))

def getLeagueHierarchy():
    fullUrl = baseUrl + f"nfl/official/trial/{version}/{languageCode}/league/hierarchy.json?api_key={apiKey}"
    
    return convertToObject(makeGetRequest(fullUrl))