import websockets, asyncio, os, json, jsonpickle, re, requests, redis, threading, uuid
from time import sleep

from components.logger import logger as mainlogger
from components.settings import settings
from components.anime import anime
from components.weather import weather
from components.messagehandler import messagehandler
import components.helpers.Q as Q

class Networking:
    def __init__(self):
        self.logger("started")
        self.q = Q.baseQueue
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
                target = msgdata["target"]
                if category == "sendmsg":
                    realdata = json.loads(msgdata["data"])
                    category = realdata["category"]
                    msgtype = realdata["type"]
                    data = realdata["data"]
                    metadata = realdata["metadata"]
                    metadata["guid"] = self.createGUID()
                    msg = {"status": 200, "category": category, "type": msgtype, "data": data, "metadata": metadata}

                pretargetlist = settings().findtarget(target)
                if pretargetlist["status"] == 200:
                    targetlist = pretargetlist["resource"]
                    for target in targetlist:
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
                #datadict["metadata"].update({"websocket":websocket})
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
                self.logger(f"message: \"{message}\" sent")
                return {"status": 200, "resource":message}
            except Exception as e:
                return {"status": 503, "resource": f"sending to {name} failed."}
        else:
            return {"status": 404, "resource": f"{name} not found"}

    def getwebsockdict(self):
        res = jsonpickle.decode(self.r.get("socketdict"))
        return res

    def createGUID(self):
        guid = str(uuid.uuid4()) #TODO onnodig
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

        
    def startserving(self):
        serveserver = websockets.server.serve(self.runserver, "0.0.0.0", 8000, loop=self.loop)
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(serveserver)
        self.loop.run_until_complete(self.msgcheck())
        self.loop.run_forever()


