import os, redis, json
from components.logger import logger as mainlogger
from components.settings import settings


class Event:
    def __init__(self): 
        self.r = redis.Redis(host="localhost", port=6379, db=0)
        self.tag = "events"
        #self.p = self.r.pubsub()

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def weather(self, msgdata):
        self.logger(f"Weather data is:\n\n {msgdata}", "debug", "yellow")
        target = "weather"
        msgdata["command"] = "weather"
        msgdata["type"] = "current" # for web
        finalmsg = json.dumps({"command":"sendmsg", "msg":msgdata, "target":target})
        self.send(finalmsg)

    def anime(self, eventtype):
        if eventtype == "aired":
            lastshow = settings().getsettings("anime", "lastshow")["resource"]
            premsgdata = settings().getsettings("anime", "maindict")["resource"][lastshow]
            msgdata = {}
            self.logger(f"Anime data is:\n\n {msgdata}", "debug", "yellow")
            target = "anime"
            msgdata["category"] = "anime"
            msgdata["type"] = "latest"
            datadict = {}
            datadict["title"] = lastshow
            datadict["lastep"] = premsgdata["lastep"]
            datadict["art"] = premsgdata["art"]
            datadict["aired_at"] = premsgdata["aired_at"]
            msgdata["data"] = datadict
            msgdata["metadata"] = {"target":"anime", "status":200}
            finalmsg = json.dumps({"command":"sendmsg", "msg":msgdata, "target":target})
            self.send(finalmsg)
        if eventtype == "compressed":
            pass

    def send(self, data):
        self.r.publish("sendmsg", data)
        self.r.publish("sendwebmsg", data)
        self.logger(f"message: {data} sent!", "debug", "yellow")

    def randomshow(self):
        # pick random show
        pass
