import redis, websockets, asyncio, os, json, jsonpickle, re, requests, redis, threading, uuid
from time import sleep

from components.logger import logger as mainlogger
from components.settings import settings
from components.anime import anime
from components.weather import weather
import components.helpers.Q as Q

class messagehandler:
    def __init__(self):
        self.websockdict = {}
        self.q = Q.baseQueue
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def logger(self, msg, type="info", colour="none"):
        self.tag = "message handler"
        mainlogger().logger(self.tag, msg, type, colour)

    async def sendbyname(self, message, name):
        if type(message) != dict:
            message = json.loads(message)
        self.logger(f"sendbyname: message: {message}")
        self.logger(self.websockdict.keys())
        if name in self.websockdict:
            self.logger(f"able to send to {name}")
            websocket = self.websockdict[name]
            try:
                await websocket.send(json.dumps(message))
                self.logger("message sent")
                return {"status": 200, "resource":message}
            except Exception as e:
                self.logger("message failed.")
                return {"status": 503, "resource": f"sending to {name} failed."}
        else:
            return {"status": 404, "resource": f"{name} not found"}

    def getwebsockdict(self):
        preres = self.r.get("socketdict").decode()
        self.logger(preres,"debug","red")
        res = jsonpickle.decode(preres)
        return res


    def createGUID(self):
        guid = str(uuid.uuid4())
        return guid

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

    def savesocket(self, ws, id):
        self.logger("Saving socket")
        self.websockdict[id] = ws
        sdict = jsonpickle.encode({id:ws})
        self.r.set("socketdict", sdict)
        self.q.put({"websockdict":self.websockdict})
        
        
        return {"status": 200, "function":"savesocket", "data":{"ws":ws, "id":id}}

    async def sendmsg(self, ws, message):
        await ws.send(message)
        self.logger(f"Message: \"{message}\" sent!")

    def messagebuilder(self, category, type, data, metadata = {}, status = "200"):
        finalmsg = json.dumps({"status":status, "category": category, "type": type, "data": data, "metadata": metadata})
        return finalmsg

    #TODO check if the reserved keyword type works here ;), furthermore, nice job on replacing this
    async def messagehandler(self, ws, message):
        self.logger(message, "debug", "blue")
        category = message["category"]
        type = message["type"]
        data = message.get("data", {}) # optional
        metadata = message["metadata"]
        id = metadata.get("id", None)
        if id:
            self.logger("updating activity..", "debug", "yellow")
            settings().updateactivity(id, True)
        address = ws.remote_address[0]
        self.logger(metadata, "info", "blue")
        self.logger(message, "debug", "yellow")
        if "guid" not in metadata: # for tracking purposes
            metadata["guid"] = self.createGUID()
            self.logger("added guid!")


        if category == "help":
            if type == "anime":
                methods = ["list", "latest", "showinfo"]
                helpdata = data.get("method") or None
                if helpdata == None:
                    message = "Please try inserting one of the methods as data, like: data:{\"method\":\"list\"}"
                    finaldict = {"status": 200, "methods": methods, "message":message, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, message, metadata)
                    await self.sendmsg(ws, finaldict)
                elif helpdata == "list":
                    message = "TODO implement help message"
                    finaldict = {"status": 200, "message":message, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, message, metadata)
                    await self.sendmsg(ws, finaldict)
                elif helpdata == "latest":
                    message = "TODO implement help message"
                    finaldict = {"status": 200, "message":message, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, message, metadata)
                    await self.sendmsg(ws, finaldict)
                elif helpdata == "showinfo":
                    message = "TODO implement help message"
                    finaldict = {"status": 200, "message":message, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, message, metadata)
                    await self.sendmsg(json.dumps(finaldict))

        if category == "admin":
            if type == "signin":
                name = data["name"]
                devtype = data["devtype"]
                subs = data["subscriptions"]
                capabilities = data["capabilities"]
                newdata = {"name":name, "devtype":devtype, "subscriptions":subs, "lastaddress":address, "capabilities":capabilities}
                result = settings().setusersettings(newdata)
                self.logger(result, "debug", "yellow")
                if result["status"] == 201: # 201 because creation
                    self.logger(result["resource"], "debug")
                    id = result["resource"]["id"]
                    settings().updateactivity(id, True)
                    category = "admin"
                    type = "signinresponse"
                    data = {"id":id}
                    metadata = {"status": 200}
                    msg = self.messagebuilder(category, type, data, metadata)
                    self.savesocket(ws, id)
                else: # maybe do different error codes here at some point
                    category = "admin"
                    type = "signinresponse"
                    data = {"resource":"failed to sign in"}
                    metadata = {"status": 503}
                    msg = self.messagebuilder(category, type, data, metadata)
                await self.sendmsg(ws, msg)
                self.logger("Sent Message!", "debug", "red")

        if category == "test":
            if type == "failure":
                data = {"message":"Failure is not acceptable"}
                finaldict = self.messagebuilder(category, type, data)
                await self.sendmsg(ws, finaldict)

            if type == "long":
                data = {"message":"Pfft that took a while.."}
                finaldict = self.messagebuilder(category, type, data)

                sleep(5)
                await self.sendmsg(ws, finaldict)

            if type == "short":
                data = {"message":"That was quick!"}
                finaldict = self.messagebuilder(category, type, data)
                await self.sendmsg(ws, finaldict)



        if category == "anime":
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
                    data = {"list":anilist}
                    finaldict = {"status": 200, "category": category, "type": type, "data":data, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, data, metadata)
                    await self.sendmsg(ws, finaldict)

                else:
                    data = {"error":"error"}
                    finaldict = {"status": 500, "category": category, "type": type, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, data, metadata)
                    await self.sendmsg(ws, finaldict)

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
                    finaldict = self.messagebuilder(category, type, showinfo, metadata)
                    await self.sendmsg(ws, finaldict)

            if type == "showinfo":
                targetshow = data["show"]
                premaindict = settings().getsettings("anime", "maindict")
                if premaindict["status"] == 200:
                    maindict = premaindict["resource"]
                    showinfo = maindict[targetshow] # might not exist
                    showinfo["title"] = targetshow
                    finaldict = {"status": 200, "category": category, "type": type, "data":showinfo, "metadata":metadata}
                    finaldict = self.messagebuilder(category, type, showinfo, metadata)
                    await self.sendmsg(ws, finaldict)

        if category == "weather": # requires a known and recent location.
            if type == "current":
                # TODO remove when implemented
                data = weather().getcurrentweather()["resource"]
                self.logger(data)
                finaldict = self.messagebuilder(category, type, data, metadata)
                await self.sendmsg(ws, finaldict)
        if category == "calendar":
            # TODO remove when implemented
            finaldict = {"status": 501, "category": category, "metadata":metadata}
            await self.sendmsg(ws, finaldict)

        if category == "monitor":
            # TODO remove when implemented
            finaldict = {"status": 501, "category": category, "metadata":metadata}
            await self.sendmsg(ws, finaldict)

        # save connection
        #TODO make above ifs into elifs and then add one final else to catch all not-known category requests
