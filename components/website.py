from flask import Flask, render_template
from flask_sockets import Sockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

try:
    from components.settings import settings
    from components.logger import logger as mainlogger
    from components.weather import weather
    from components.messagehandler import messagehandler
    import components.helpers.Q as Q
except:
    from settings import settings
    from logger import logger as mainlogger
    from weather import weather
    from messagehandler import messagehandler
    import helpers.Q as Q
import asyncio, sys, os, json, redis, threading, traceback, uuid, random
from time import sleep

#TODO on many places you create variables you do not use later on. Avoid this and refactor them into direct assignments
#TODO put an else at the end of all your else-ifs, to catch any unwanted messages
#TODO put all the status-codes into an Enum (you can document the codes here as well very nicely)

class website:
    def __init__(self):
        self.q = Q.baseQueue
        self.app = Flask(__name__)
        self.sockets = Sockets(self.app)
        self.MsgHandler = messagehandler()
        #self.socketdict = {}
        self.socketlist = []
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.p.subscribe("sendwebmsg")

    def logger(self, msg, type="info", colour="none"):
        self.tag = "website"
        mainlogger().logger(self.tag, msg, type, colour)

    def msgcheck(self):
        # pubsub checker to send messages
        while True:
            msg = self.p.get_message()
            if msg and type(msg["data"]) != int:
                msgdata = json.loads(msg["data"].decode())
                category = msgdata["category"]
                target = msgdata["target"]
                if category == "sendmsg":
                    realdata = json.loads(msgdata["data"])
                    category = realdata["category"]
                    msgtype = realdata["type"]
                    data = realdata["data"]
                    metadata = realdata["metadata"]
                    metadata["guid"] = self.createGUID()
                    msg = {"status": 200, "category": category, "type": msgtype, "data": data, "metadata": metadata}
                    for ws in self.q.get()["websockdict"]:
                        self.sendmsg(ws, msg)
            sleep(3)

    def loopfunc(self):
        self.logger("in loop func!", "info", "blue")
        while True:
            lst = settings().getsettings("anime", "maindict")["resource"]

            chosenshow = list(lst.keys())[random.randint(0, len(lst)-1)]
            preshowdict = lst[chosenshow]

            title = chosenshow
            imagelink = preshowdict["art"]["cover"]
            bannerlink = preshowdict["art"]["banner"]
            episode = preshowdict["lastep"]
            timestamp = preshowdict["aired_at"]

            showdict = {"title":title, "lastep": episode, "aired_at": timestamp, "art":{"cover": imagelink, "banner": bannerlink}}
            category = "tests"
            type = "replace"
            metadata = {"target":"anime", "guid": self.createGUID()}
            finaldict = {"status": 200, "command": category, "type": type, "data":showdict, "metadata": metadata}

            for ws in self.socketlist:
                self.sendmsg(ws, finaldict)


            # weather
            #results = weather().getcurrentweather()["resource"]
            #self.logger(results)

            #metadata = {"target":"weather", "guid": self.createGUID()}

            #finaldict = {"status": 200, "category": "weather", "type": "current", "data": results, "metadata":metadata}
            #for ws in self.socketlist:
                #self.sendmsg(ws, finaldict)

            sleep(15)

    def sendmsg(self, ws, msg):
        try:
            ws.send(json.dumps(msg))
        except Exception as e:
            # handle this properly
            self.logger(e, "alert", "red")
            self.socketlist.remove(ws)

    def createGUID(self):
        guid = str(uuid.uuid4()) #TODO onnodig
        return guid

    #TODO extract this into its own class, as it is going to get pretty huge.
    # make a single Handle() and then just call MessageHandler.Handle(ws, message)
    def messagehandler(self, ws, message):
            message = json.loads(message)

            category = message["category"]
            type = message["type"]
            data = message.get("data", {}) # optional
            metadata = message.get("metadata", {}) # optional

            self.logger(metadata, "info", "blue")
            if "guid" not in metadata: # for tracking purposes
                metadata["guid"] = self.createGUID()
                self.logger("added guid!")
            
                
            if category == "admin":
                if type == "signin":
                    #TODO implement sign in process
                    pass
            if category == "test":
                if type == "failure":
                    finaldict = {"status": 406, "category": category, "type": type, "data":{"message":"Failure is not acceptable"}}
                    self.sendmsg(ws, finaldict)

                if type == "long":
                    finaldict = {"status": 200, "category": category, "type": type, "data":{"message":"Pfft that took a while.."}}
                    sleep(5)
                    self.sendmsg(ws, finaldict)

                if type == "short":
                    finaldict = {"status": 200, "category": category, "type": type, "data":{"message":"That was quick!"}}
                    self.sendmsg(ws, finaldict)

            if category == "anime":
                if type == "help":
                    methods = ["list", "latest", "showinfo"]
                    helpdata = data["method"] or None
                    if helpdata == None:
                        message = "Please try inserting one of the methods as data, like: data:{\"method\":\"list\"}"
                        finaldict = {"status": 200, "methods": methods, "message":message, "metadata":metadata}
                        self.sendmsg(ws, finaldict)
                    elif helpdata == "list":
                        message = "TODO implement help message"
                        finaldict = {"status": 200, "message":message, "metadata":metadata}
                        self.sendmsg(ws, finaldict)
                    elif helpdata == "latest":
                        message = "TODO implement help message"
                        finaldict = {"status": 200, "message":message, "metadata":metadata}
                        self.sendmsg(ws, finaldict)
                    elif helpdata == "showinfo":
                        message = "TODO implement help message"
                        finaldict = {"status": 200, "message":message, "metadata":metadata}
                        self.sendmsg(json.dumps(finaldict))

                if type == "list":
                    prenamelist = settings().getsettings("anime", "list")
                    preanimedict = settings().getsettings("anime", "maindict")
                    if prenamelist["status"] == 200:
                        anilist = []
                        namelist = prenamelist["resource"]
                        maindict = preanimedict["resource"]
                        for name in namelist:
                            if name in maindict:
                                entry = maindict[name]
                                entry["title"] = name
                                anilist.append(entry)
                        finaldict = {"status": 200, "category": category, "type": type, "data":{"list":anilist}, "metadata":metadata}
                        self.sendmsg(ws, finaldict)

                        #TODO remove this testing message
                        finaldict = {"status": 406, "message":"Failure is not acceptable"}
                        self.sendmsg(ws, finaldict)

                    else:
                        finaldict = {"status": 500, "category": category, "type": type, "metadata":metadata}
                        self.sendmsg(ws, finaldict)

                if type == "latest":
                    preanidict = settings().getsettings("anime") # get full anime dict
                    if preanidict["status"] == 200:

                        anidict = preanidict["resource"]
                        latestshow = anidict["lastshow"] # catch errors for these
                        anilist = anidict["list"]
                        maindict = anidict["maindict"]
                        showinfo = maindict[latestshow]
                        showinfo["title"] = latestshow
                        finaldict = {"status": 200, "category": category, "type": type, "data":showinfo, "metadata": metadata}
                        self.sendmsg(ws, finaldict)

                if type == "showinfo":
                    targetshow = data["show"]
                    premaindict = settings().getsettings("anime", "maindict")
                    if premaindict["status"] == 200:
                        maindict = premaindict["resource"]
                        showinfo = maindict[targetshow] # might not exist
                        showinfo["title"] = targetshow
                        finaldict = {"status": 200, "category": category, "type": type, "data":showinfo, "metadata":metadata}
                        self.sendmsg(ws, finaldict)

            if category == "weather":
                # TODO remove when implemented
                results = weather().getcurrentweather()["resource"]
                self.logger(results)
                finaldict = {"status": 200, "category": category, "type": "current", "data": results, "metadata":metadata}

                self.sendmsg(ws, finaldict)

                if type == "current": # require data to include location
                    # TODO implement
                    pass

            if category == "calendar":
                # TODO remove when implemented
                finaldict = {"status": 501, "category": category, "metadata":metadata}
                self.sendmsg(ws, finaldict)

            if category == "monitor":
                # TODO remove when implemented
                finaldict = {"status": 501, "category": category, "metadata":metadata}
                self.sendmsg(ws, finaldict)

            #TODO make above ifs into elifs and then add one final else to catch all not-known category requests


    def websocklistener(self):
        pass

    def runserver(self):

        threading.Thread(target=self.loopfunc).start()
        threading.Thread(target=self.msgcheck).start()
        """
        @self.sockets.route('/')
        async def socket(ws):
            try:
                while not ws.closed:
                    message = ws.receive()
                    if message:
                        self.logger(f"Message received: {message}")
                        if ws not in self.socketlist:
                            self.socketlist.append(ws)
                        await self.MsgHandler.messagehandler(ws, message)
            #except webSocketError:
            #    self.logger("lost connection!")
            except Exception as e:
                self.logger(e, "alert", "red")
                traceback.print_exc()
                self.logger(e.__class__.__name__)
        """
        @self.app.route('/')
        def hello():
            return render_template("index.html")


        server = pywsgi.WSGIServer(('0.0.0.0', 8080), self.app, handler_class=WebSocketHandler)
        server.serve_forever()

if __name__ == "__main__":
    website().logger("Starting as standalone", "info", "blue")
    website().runserver()
