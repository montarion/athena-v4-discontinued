import os, redis, json
from components.logger import logger as mainlogger
class Event:
    def __init__(self): 
        self.r = redis.Redis(host="localhost", port=6379, db=0)
        self.tag = "events"
        #self.p = self.r.pubsub()

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def anime(self):
        msgdata = json.loads(self.r.get("lastshow").decode())
        target = "anime"
        msgdata["command"] = "anime"
        finalmsg = json.dumps({"command":"sendmsg", "msg":msgdata, "target":target})
        self.send(finalmsg)

    def send(self, data):
        self.r.publish("sendmsg", data)
        self.logger(f"message: {data} sent!", "debug", "yellow")
