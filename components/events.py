import os, redis, json, asyncio
from components.logger import logger as mainlogger
from components.settings import settings
import components.helpers.Q as Q

class Event:
    def __init__(self): 
        self.q = Q.baseQueue
        self.r = redis.Redis(host="localhost", port=6379, db=0)
        self.tag = "events"
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        #self.p = self.r.pubsub()

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def weather(self, msgdata): 
        target = "weather"
        finaldict = self.messagebuilder("weather", "current", msgdata)
        finalmsg = {"category":"sendmsg", "data":finaldict, "target":target}
        self.send(finalmsg)

    def anime(self, eventtype):
        if eventtype == "aired":
            lastshow = settings().getsettings("anime", "lastshow")["resource"]
            premsgdata = settings().getsettings("anime", "maindict")["resource"][lastshow]
            msgdata = {}
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
            #finalmsg = json.dumps({"command":"sendmsg", "msg":msgdata, "target":target})
            finalmsg = {"command":"sendmsg", "msg":msgdata, "target":target}
            self.send(finalmsg)
        if eventtype == "compressed":
            pass

    def send(self, data):
        target = data["target"]
        msg = data["data"]
        pretlist = settings().findtarget(target)
        self.logger(pretlist["status"] == 200, "debug", "yellow")
        if pretlist["status"] == 200:
            self.logger("here")
            try:
                wsdict = self.q.get(False)["websockdict"]
            except Exception as e:
                self.logger(e)
                return
            #self.q.put(wsdict, False) # always put it back
            tlist = pretlist["resource"]
            self.logger(wsdict)
            for t in tlist:
                self.logger(t)
                try:
                    ws = wsdict[t]
                    self.logger("websocket found")
                    self.loop.run_until_complete(ws.send(msg))
                    self.logger("sent")
                except:
                    wsdict.pop(t, "")
            self.q.put({"websockdict":wsdict}) # always put it back


    def redissend(self, data):
        self.r.publish("sendmsg", data)
        self.r.publish("sendwebmsg", data)

    def randomshow(self):
        # pick random show
        pass

    def messagebuilder(self, category, type, data, metadata = {}, status = "200"):
        finalmsg = json.dumps({"status":status, "category": category, "type": type, "data": data, "metadata": metadata})
        return finalmsg

#TODO hier mooi voorbeeld van veel variabelen om een message te maken, builder pattern te gebruiken. Try it out
