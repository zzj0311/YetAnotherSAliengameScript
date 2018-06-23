# YetAnotherSAliengameScript
A python based script to auto send score to the steam summer sale saliengame

## Usage
```
python3 sAlien.py -k YOURTOKEN -s SERVERJIANGSCKEY
```
## What I have done
* basic api requests
* a time-in-planet based strategy (this means the script won't exit a planet until the planet is dead)
* automatically choose the present highest score zone (top-bottom rule)
* a simple notification service based on server酱

## What I won't do
* Answer any script unrelated issue
* pack it into a excutable file
* Add gui or something complicated but useless

## Where to hold?
Technically it runs on any devices which allows python3 code, which includes almost all devices we can see daily, such as your android phone if you want. I personally recommend a PI-like embeded device or a vps server with a Linux system, of course windows is also supported, technically.

To get it work, you should get your steam game token first. visit [this site](https://steamcommunity.com/saliengame/gettoken) in your browser and you can see something like this:
```
{
    "webapi_host": "https://community.steam-api.com/", 
    "webapi_host_secure": "https://community.steam-api.com/", 
    "token": "YOURTOKENHERE", 
    "steamid": "YOURSTEAMID", 
    "persona_name": "YOURSTEAMUSERNAME", 
    "success": 1
}
```
get your token and let's get started.

## Preparation
* get python, install requests
```
sudo apt-get update && upgrade
apt-get install python3 python3-pip
pip3 install requests
```

For win10 users, I recommend you to use the windows sub linux and follow my guide above if you have no idea how to use Linux or python.

* get server酱 SCKEY (optional)

visit [this site](http://sc.ftqq.com/3.version) and follow the instruction there to get your key, there's no need to finish this step if you don't need a notification service. In the script I send notification when:

1. every 100 score sent, your salien's current state is sent to your wechat;
2. a request failed for 5 times, which indicates the steam-api is temporaily not reachable;
3. the whole planet is dead and you have to manually enter a new one (so you can choose your preferred games to paticipate).

and you can replace the part after -s in usage to enjoy a simple notification service then.

