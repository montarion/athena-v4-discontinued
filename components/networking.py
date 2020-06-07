import websockets, asyncio, os, json, jsonpickle, re, requests, redis, threading
from time import sleep

from components.logger import logger as mainlogger
from components.settings import settings
from components.anime import anime
from components.weather import weather
from components.messagehandler import messagehandler

class Networking:
    def __init__(self):
        self.logger("started")
        self.MsgHandler = messagehandler()
        self.userdict = {}
        self.loop = asyncio.new_event_loop()
        self.websockdict = {}
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.tag = "networking"
        # subs
        self.p.subscribe("sendmsg")
        #p.run_in_thread(sleep_time=0.1)

    def logger(self, msg, type="info", colour="none"):
        self.tag = "networking"
        mainlogger().logger(self.tag, msg, type, colour)

    async def msgcheck(self):
        self.logger("pubsub started")
        # pubsub checker to send messages
        while True:
            msg = self.p.get_message()
            if msg and type(msg["data"]) != int:
                msgdata = json.loads(msg["data"].decode())
                category = msgdata["category"]
                msgtype = msgdata["type"]
                data = msgdata["data"]
                metadata = msgdata.get("metadata",{})
                target = msgdata["target"]
                self.logger(msgdata, "debug", "red")
                msg = {"category":category, "type":msgtype, "data":data, "metadata":metadata}
                self.logger(f"message is: \n{msg}")
                pretargetlist = settings().findtarget(target)
                if pretargetlist["status"] == 200:
                    targetlist = pretargetlist["resource"]
                    for target in targetlist:
                        self.logger(f"target is: {target}")
                        await self.MsgHandler.sendbyname(msg, target)
                else:
                    self.logger(pretargetlist["resource"])

            await asyncio.sleep(3)

    async def runserver(self, websocket, path):
        self.logger("in server")
        try:
            while True:
                data = await websocket.recv()
                self.logger(data, "debug", "yellow")
                datadict = json.loads(str(data))
                if "metadata" not in datadict:
                    datadict["metadata"] = {}
                datadict["metadata"].update({"websocket":websocket})
                await self.MsgHandler.messagehandler(websocket, datadict)
        except Exception as e:
            self.logger("ERROR", "alert", "red")
            pattern = "code = ([0-9]*).*"
            self.logger(e, "debug", "red")
            searchres = re.search(pattern, str(e))
            realerror = searchres.group(1)

            self.logger(realerror, "debug", "red")
            if realerror == "1006":
                self.logger("Connection closed by peer.")
                #await websocket.close(4000)
            elif realerror == "4000":
                self.logger("Connection reset.")
                #await websocket.close(4000)
            else:
                self.logger(e)
                #await websocket.close(4000)
        

    async def send(self, message, websocket):
        await websocket.send(message)
        self.logger("message sent")

    async def sendbyname(self, message, name):
        if type(message) != dict:
            message = json.loads(message)
        self.logger(f"sendbyname: message: {message}")
        websockdict = self.getwebsockdict
        if name in websockdict:
            websocket = websockdict[name]
            try:
                await websocket.send(json.dumps(message))
                self.logger("message sent")
                return {"status": 200, "resource":message}
            except Exception as e:
                return {"status": 503, "resource": f"sending to {name} failed."}
        else:
            return {"status": 404, "resource": f"{name} not found"}

    def getwebsockdict(self):
        res = jsonpickle.decode(self.r.get("socketdict"))
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
            type = userdict[machine]["devtype"]
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

    async def oldmessagehandler(self, messagedict):
        command = messagedict["operation"] #TODO: make this lists, so you can accept multiple commands at a time

        if command == "signin":
            self.logger("Got sign in request!")
            name = messagedict["data"]["name"]
            type = messagedict["data"]["type"]
            subs = messagedict["data"]["subscriptions"]
            capabilities = messagedict["data"]["capabilities"]
            websocket = messagedict["metadata"]["websocket"]
            address = websocket.remote_address[0]
            if name in self.websockdict:
                self.logger(f"closing old websocket for {name}")
                #await self.websockdict[name].close(4000)
            self.websockdict[name] = websocket
            
            # TODO: make this respond to what the user has actually sent(something might be missing)
            newdata = {"type":type, "subscriptions":subs, "lastaddress":address, "capabilities":capabilities}
            result = settings().setusersettings(name, newdata)
            if result["status"] == 201: # 201 because creation
                self.logger(result["resource"], "debug")
                id = result["resource"]["id"]
                msg = json.dumps({"status":200, "command":"signin", "id":id})
            else: # maybe do different error codes here at some point
                msg = json.dumps({"status":503, "resource":"failed to sign in", "command":"signin"})
            await self.send(msg, messagedict["metadata"]["websocket"])

        if command == "anime":
            id = str(messagedict["id"])
            numberofshows = 1
            if "data" in messagedict.keys():
                numberofshows = messagedict["data"]["shows"]
            targetlist = self.findtarget(id)
            if len(targetlist) > 0:
                animeresults = anime().getshows(numberofshows)
                animeresults["command"] = "anime"
                self.logger(f"targetlist: {targetlist}")
                for target in targetlist:
                    await self.sendbyname(animeresults, target)

        if command == "weather":
            senddict = {"command": "weather"}
            id = str(messagedict["id"])
            targetlist = self.findtarget(id)
            if len(targetlist) > 0:
                weatherresults = weather().getcurrentweather()["resource"]
                weatherresults["command"] = "weather"
                self.logger(f"targetlist: {targetlist}")
                for target in targetlist:
                    await self.sendbyname(weatherresults, target)

        
    def startserving(self):
        serveserver = websockets.server.serve(self.runserver, "0.0.0.0", 8000, loop=self.loop)
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(serveserver)
        self.loop.run_until_complete(self.msgcheck())
        self.loop.run_forever()


