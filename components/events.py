import os, redis, json
from components.logger import logger as mainlogger
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
    def anime(self, msgdata):
        #msgdata = json.loads(self.r.get("lastshow").decode())
        self.logger(f"Anime data is:\n\n {msgdata}", "debug", "yellow")
        target = "anime"
        msgdata["command"] = "anime"
        msgdata["type"] = "latest" # for web
        finalmsg = json.dumps({"command":"sendmsg", "msg":msgdata, "target":target})
        self.send(finalmsg)

    def send(self, data):
        self.r.publish("sendmsg", data)
        self.r.publish("sendwebmsg", data)
        self.logger(f"message: {data} sent!", "debug", "yellow")

    def randomshow(self):
        # pick random show
        pass

#TODO hier mooi voorbeeld van veel variabelen om een message te maken, builder pattern te gebruiken. Try it out