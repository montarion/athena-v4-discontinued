from flask import Flask, render_template
from flask_sockets import Sockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

try:
    from components.settings import settings
    from components.logger import logger as mainlogger
except:
    from settings import settings
    from logger import logger as mainlogger

import sys, os, json, redis, threading, traceback, uuid
from time import sleep

class website:
    def __init__(self):
        self.app = Flask(__name__)
        self.sockets = Sockets(self.app)

    def logger(self, msg, type="info", colour="none"):
        self.tag = "website"
        mainlogger().logger(self.tag, msg, type, colour)

    def sendmsg(self, ws, msg):

        ws.send(json.dumps(msg))

    def createGUID(self):
        guid = str(uuid.uuid4())
        return guid

    def messagehandler(self, ws, message):
            message = json.loads(message)

            category = message["category"]
            type = message["type"]
            data = message.get("data", {}) # optional
            metadata = message.get("metadata", {}) # optional

            if "guid" not in metadata: # for tracking purposes
                metadata["guid"] = self.createGUID()
                self.logger("added guid!")
            
            if category == "test":
                if type == "failure":
                    finaldict = {"status": 406, "message":"Failure is not acceptable"}
                    self.sendmsg(ws, finaldict)

                if type == "long":
                    finaldict = {"status": 200, "message":"Pfft that took a while.."}
                    sleep(5)
                    self.sendmsg(ws, finaldict)

                if type == "short":
                    finaldict = {"status": 200, "message":"That was quick!"}
                    self.sendmsg(ws, finaldict)

            if category == "anime":
                if type == "help":
                    methods = ["list", "latest", "showinfo"]
                    helpdata = data["method"] or None
                    if helpdata == None:
                        message = "Please try inserting one of the methods as data, like: data:{\"method\":\"list\"}"
                        finaldict = {"status": 200, "methods": methods, "message":message}
                        self.sendmsg(ws, finaldict)
                    elif helpdata == "list":
                        message = "TODO implement help message"
                        finaldict = {"status": 200, "message":message}
                        self.sendmsg(ws, finaldict)
                    elif helpdata == "latest":
                        message = "TODO implement help message"
                        finaldict = {"status": 200, "message":message}
                        self.sendmsg(ws, finaldict)
                    elif helpdata == "showinfo":
                        message = "TODO implement help message"
                        finaldict = {"status": 200, "message":message}
                        self.sendmsg(json.dumps(finaldict))

                if type == "list":
                    preanilist = settings().getsettings("anime", "list")
                    if preanilist["status"] == 200:
                        anilist = preanilist["resource"]
                        finaldict = {"status": 200, "category": category, "type": type, "data":{"list":anilist}}
                        self.sendmsg(ws, finaldict)
                        finaldict = {"status": 406, "message":"Failure is not acceptable"}
                        self.sendmsg(ws, finaldict)

                    else:
                        finaldict = {"status": 500, "category": category, "type": type}
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
                        finaldict = {"status": 200, "category": category, "type": type, "data":showinfo}
                        self.sendmsg(ws, finaldict)
                        finaldict = {"status": 406, "message":"Failure is not acceptable"}
                        self.sendmsg(ws, finaldict)


                if type == "showinfo":
                    targetshow = data["show"]
                    premaindict = settings().getsettings("anime", "maindict")
                    if premaindict["status"] == 200:
                        maindict = premaindict["resource"]
                        showinfo = maindict[targetshow] # might not exist
                        showinfo["title"] = targetshow
                        finaldict = {"status": 200, "category": category, "type": type, "data":showinfo}
                        self.sendmsg(ws, finaldict)

            if category == "weather":
                # TODO remove when implemented
                finaldict = {"status": 501, "category": category}
                self.sendmsg(ws, finaldict)

                if type == "current": # require data to include location
                    # TODO implement
                    pass

            if category == "calendar":
                # TODO remove when implemented
                finaldict = {"status": 501, "category": category}
                self.sendmsg(ws, finaldict)

            if category == "monitor":
                # TODO remove when implemented
                finaldict = {"status": 501, "category": category}
                self.sendmsg(ws, finaldict)


    def runserver(self):

        @self.sockets.route('/')
        def socket(ws):
            try:
                while not ws.closed:
                    message = ws.receive()
                    if message:
                        self.logger(f"Message received: {message}")
                        self.messagehandler(ws, message)
            #except webSocketError:
            #    self.logger("lost connection!")
            except Exception as e:
                self.logger(e, "alert", "red")
                traceback.print_exc()
                self.logger(e.__class__.__name__)

        @self.app.route('/')
        def hello():
            return render_template("index.html")


        server = pywsgi.WSGIServer(('0.0.0.0', 8080), self.app, handler_class=WebSocketHandler)
        server.serve_forever()

if __name__ == "__main__":
    website().logger("Starting as standalone", "info", "blue")
    website().runserver()
