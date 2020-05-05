import redis, websockets, asyncio, os, json, re, requests, redis, threading
from time import sleep

from components.logger import logger as mainlogger
from components.settings import settings

class messagehandler:
    def __init__(self):
        self.websockdict = {}

    def logger(self, msg, type="info", colour="none"):
        self.tag = "message handler"
        mainlogger().logger(self.tag, msg, type, colour)

    async def sendbyname(self, message, name):
        if type(message) != dict:
            message = json.loads(message)
        self.logger(f"sendbyname: message: {message}")
        if name in self.websockdict:
            websocket = self.websockdict[name]
            try:
                await websocket.send(json.dumps(message))
                self.logger("message sent")
                return {"status": 200, "resource":message}
            except Exception as e:
                return {"status": 503, "resource": f"sending to {name} failed."}
        else:
            return {"status": 404, "resource": f"{name} not found"}

    async def getwebsockdict(self):
        res = self.websockdict
        return res

    def findtarget(self, search):
        search = str(search)
        finalnames = []
        with open("data/userstore.json", "r") as f:
            userdict = json.loads(f.read())

        for machine in userdict:
            name = machine
            capabilities = userdict[machine]["capabilities"]
            subscription = userdict[machine]["subscriptions"]
            type = userdict[machine]["type"]
            id = userdict[machine]["id"]
            if search == name:
                finalnames.append(machine)
            elif search in capabilities:
                finalnames.append(machine)
            elif search in subscription:
                finalnames.append(machine)
            elif search in type:
                finalnames.append(machine)
            elif search in str(id):
                finalnames.append(machine)
        return finalnames


    #TODO check if the reserved keyword type works here ;), furthermore, nice job on replacing this
    async def messagehandler(self, ws, message):
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
            if type == "weather":
                results = weather().getcurrentweather()["resource"]
                self.logger(results)

                finaldict = {"status": 200, "category": category, "type": "current", "data": results, "metadata":metadata}

                self.sendmsg(ws, finaldict)
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
