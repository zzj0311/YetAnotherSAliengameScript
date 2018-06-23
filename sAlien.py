#!/usr/bin/python3
import requests
import argparse
import time
import json

parser = argparse.ArgumentParser()
parser.add_argument("--token", "-k", dest = "token", default = "")
parser.add_argument("--server-jiang", "-s", dest = "serverToken", default = "")
args = parser.parse_args()

scoreList = [595, 1190, 2380]
if args.token == "":
    print("You should pass token through args to continue, exp: salien.py -k YOURTOKENHERE")
    exit()

r = requests.session()
r.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US; Valve Steam Client/default/1529009056; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer': 'https://steamcommunity.com/saliengame/play/',
    'Origin': 'https://steamcommunity.com',
    'Accept': '*/*'
})
def sendNote(title, text):
    if args.serverToken == "":
        return
    url = "https://sc.ftqq.com/{0}.send?text={1}&desp={2}".format(args.serverToken, title, text)
    print(url)
    requests.get(url)
    return

def sendPost(method, data):
    flag = 1
    count = 0
    while flag and count < 5:
        try:
            response = r.post('https://community.steam-api.com/ITerritoryControlMinigameService/{}/v0001/'.format(method), data=data, timeout=10).text
            flag = 0
        except:
#            logging.debug("Something went Wrong! Retry...")
            print("Retry....")
            time.sleep(2)
            count += 1
    if count == 5:
#        logging.debug("Failed to communicate after 5 times, return...")
        print("Service temporarily not reachable, plz retry a few mins later. exit...")
        sendNote("salienError", "Service temporarily not reachable, plz retry a few mins later.")
        exit()
    response = json.loads(response)['response']
    if response == {}:
#       longging.debug("Empty response! return...")
        print("Got an empty response, return...")        
        return False, response
    else:
        return True, response

def getPlayerInfoinPlanet():
    flag, resp = sendPost("GetPlayerInfo", {'access_token':args.token, 'language':'schinese'})
    while not flag:
        flag, resp = sendPost("GetPlayerInfo", {'access_token':args.token, 'language':'schinese'})
    try:
        return resp['active_planet'], resp['score'], resp['next_level_score'], str(resp['level']), str(resp['time_on_planet'])
    except KeyError:
        return -1, resp['score'], resp['next_level_score'], str(resp['level']), -1

def getPlanetInfoinZone():
    flag, resp = sendPost("GetPlayerInfo", {'access_token':args.token, 'language':'schinese'})
    while not flag:
        flag, resp = sendPost("GetPlayerInfo", {'access_token':args.token, 'language':'schinese'})
    try:
        return resp['time_in_zone']
    except KeyError:
        print("Current zone already dead, retry...")
        return -1

def getPlanetInfo():
    id, cScore, nxtScore, lvl, timeonPlanet = getPlayerInfoinPlanet()
    if id == -1:
        return -1
    print("current active planet: {0}, player score: {1}/{2}(lv: {3}), time on planet {0}: {4}".format(id, cScore, nxtScore, lvl, timeonPlanet))
    resp = r.get("https://community.steam-api.com/ITerritoryControlMinigameService/GetPlanet/v0001/?id={}&language=schinese".format(id)).text
    resp = json.loads(resp)['response']
    return sorted([i for i in resp['planets'][0]['zones'] if i['capture_progress'] < 0.95], key = lambda x: x['difficulty'], reverse=True)[0]['zone_position']

def waitAndRetry():
    id = getPlanetInfo()
    count = 0
    while id == -1:
        time.sleep(60)
        id = getPlanetInfo()
        if count % 60 == 0:
            sendNote("salienCritical!", "One Planet is over, plz enter a new one manually")
        count += 1

def joinZone():
    id = getPlanetInfo()
    if id == -1:
        print("current planet is over, wait until enter a new one!")
        waitAndRetry()
    flag, resp = sendPost("JoinZone", {'zone_position':id, 'access_token':args.token})
    while not flag:
        print("Wait until entity available!")
        time.sleep(5)
        flag, resp = sendPost("JoinZone", {'zone_position':id, 'access_token':args.token})
    
    print("join zone success! current in zone {0}, wait around 120s and send score: {1}".format(id, scoreList[resp['zone_info']['difficulty']-1]))
    return scoreList[resp['zone_info']['difficulty']-1]

def sendScore(futureScore):
    timeinZone = getPlanetInfoinZone()
    if timeinZone == -1:
        return
    timeRemain = 115 - getPlanetInfoinZone()
    time.sleep(timeRemain)
    flag, __ = sendPost("ReportScore", {'access_token':args.token, 'score': futureScore, 'language':'schinese'})
    while not flag:
        print("Send score failed, retry...")
        time.sleep(1)
        timeinZone = getPlanetInfoinZone()
        if 120 - timeinZone < -10:
            print("Failed")
            return
        flag, __ = sendPost("ReportScore", {'access_token':args.token, 'score': futureScore, 'language':'schinese'})

    return

counter = 0
while True:
    nxt = joinZone()
    time.sleep(110 - getPlanetInfoinZone())
    sendScore(nxt)
    if counter % 100 == 0:
        id, cScore, nxtScore, lvl, timeonPlanet = getPlayerInfoinPlanet()
        sendNote("salienNormal", "current active planet: {0}, player score: {1}/{2}(lv: {3}), time on planet {0}: {4}".format(id, cScore, nxtScore, lvl, timeonPlanet))
    counter += 1
