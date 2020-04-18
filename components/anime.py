import os, requests, json, redis, feedparser, re

from components.logger import logger as mainlogger
from components.settings import settings

class anime:
    def __init__(self):
        self.tag = "anime"
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.publishchoice = "HorribleSubs"
        self.firstshow = True
        self.watchall = False # change to true to look for all shows
        prelist = settings().getsettings("anime", "list")
        if prelist["status"] == 200:
            self.watchlist = prelist["resource"]
        else:
            # alert user
            self.watchlist = self.findshows()
        predict = settings().getsettings("anime", None)
        if predict["status"] == 200:
            self.maindict = predict["resource"]["maindict"]
            #self.maindict = predict["resource"]
            self.animedict = predict["resource"]
        else:
            self.maindict = {}
        #self.maindict = #json.loads(self.r.get("animedict"))

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def getshows(self, number = 1):
        base = f"https://nyaa.si/?page=rss&q={self.publishchoice}+%2B+[1080p]&c=1_2&f=2"
        feed = feedparser.parse(base)
        entries = feed.entries
        sessiondict = {}
        for x in range(0, number):
            entry = entries[x]
            title, show, episode = self.cleantitle(entry["title"])
            link = entry["link"]
            if self.watchall:
                self.watchlist.append(show)
            if show in self.watchlist:
                sessiondict["command"] = "anime"
                sessiondict["title"] = show
                sessiondict["episode"] = episode
                if show not in self.maindict:
                    imagelink, bannerlink, maxepisodes = self.getinfo(show) #TODO add synopsis
                    self.maindict[show] = {"art":{}, "meta":{}}
                    self.maindict[show]["art"]["cover"] = imagelink
                    self.maindict[show]["art"]["banner"] = bannerlink
                    self.maindict[show]["meta"]["maxepisodes"] = maxepisodes
                sessiondict["imagelink"] = self.maindict[show]["art"]["cover"]
                sessiondict["bannerlink"] = self.maindict[show]["art"]["banner"]

                self.maindict[show]["lastep"] = episode
                if self.animedict.get("lastshow", "show") != show:
                    self.download(show, link)
                if self.firstshow:
                    self.firstshow = False
                    settings().setsettings("anime", "lastshow", show)
                    self.r.set("lastshow", json.dumps(sessiondict))
                    
        self.r.set("animedict", json.dumps(self.maindict))
        settings().setsettings("anime", "maindict", self.maindict)
        
        return sessiondict

    def cleantitle(self, title):
        pattern = "\[HorribleSubs\] (.*) - ([0-9]*) \[1080p\].mkv"
        res = re.search(pattern, title)
        show = res.group(1)
        episode = res.group(2)
        newtitle = f"{show} - {episode}.mkv"
        return newtitle, show, episode

    def getinfo(self, name):
        query = "query($title: String){Media (search: $title, type: ANIME){episodes, bannerImage, coverImage{extraLarge}}}" # this is graphQL, not REST
        variables = {'title': name}
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables})
        preurl = json.loads(response.text)["data"]["Media"]

        coverdict = preurl["coverImage"]
        bannerurl = preurl["bannerImage"]
        maxepisodes = preurl["episodes"]

        coverurl = coverdict[list(coverdict.keys())[0]]
        if bannerurl == None:
            bannerurl = coverurl

        return coverurl, bannerurl, maxepisodes


    def download(self, show, link):

        # check if folder exists:
        root = "/mnt/raspidisk/files/anime/"
        truepath = os.path.join(root, "\ ".join(show.split(" ")))
        check = os.path.isdir(truepath)
        if not check:
            self.logger("creating folder for {}".format(show), "debug")
            precommand = "sudo -H -u pi bash -c \""
            command = "mkdir {}".format(truepath)
            postcommand = "\""
            os.system(precommand + command + postcommand)
        else:
            self.logger("folder {} already existed".format(show), "debug")

        precommand = "sudo -H -u pi bash -c \""
        command = (precommand + r"deluge-console 'add -p {} {}'".format(truepath, link) + "\"")
        os.system(command)

    def findshows(self):
        from bs4 import BeautifulSoup

        url = "https://horriblesubs.info/current-season/"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        preshows = soup.find_all(class_="ind-show")
        showlist = []
        chosenlist = []
        for show in preshows:
            showlist.append(show.find("a")["title"])

        for i, show in enumerate(showlist):
            print("Show number {} is: {}".format(i + 1, show))
            interest = input("w to add {}".format(show))
            if interest == "w":
                chosenlist.append(show)
        result = settings().setsettings("anime", "list", chosenlist)
        
        return result

