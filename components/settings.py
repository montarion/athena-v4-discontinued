import os, json, redis
from time import sleep
try:
    from components.logger import logger as mainlogger
    import components.helpers.Q as Q
except:
    from logger import logger as mainlogger
    import helpers.Q as Q

class settings:
    def __init__(self):
        self.q = Q.baseQueue
        self.tag = "settings"
        self.settingsfile = "data/settings.json"
        self.userstore = "data/userstore.json"

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def updateactivity(self, id, active):
        presetting = self.getusersettings(id)
        self.logger(f"updating activity for id: {id}", "debug", "yellow")
        if presetting["status"] == 200:
            setting = presetting["resource"]
            setting["active"] = active
            # write back
            self.setusersettings(setting, id)
            return {"status": 200, "resource": setting}
        else:
            return {"status":404, "resource": f"Couldn't find: {id}"}


    def checkavailability(self, target, checknow = False):
        if checknow: # send message with callback
            pass # implement call back system
        self.logger(f"checking availibility for target: {target}", "debug", "yellow")
        preidlist = self.findtarget(target)
        userlist = self.getusersettings()["resource"]
        finallist = []
        if preidlist["status"] == 200:
            targetlist = preidlist["resource"]
            for t in targetlist:
                user = userlist[t]
                
                if user["active"] == True:
                    finallist.append(user)
                    pass
            return {"status": 200, "resource": finallist}
        return {"status":404, "resource": f"Couldn't find any machine suitable for: {target}"}


    def getsettings(self, category, item = None):
        with open(self.settingsfile) as f:
            data = json.loads(f.read())

        if category in data:
            catdata = data[category]
            if item == None:
                return {"status": 200, "resource": catdata}
            if item in catdata:
                return {"status": 200, "resource": catdata[item]}
            else:
                return {"status":404, "resource": f"Couldn't find: {item}"}
        else:
            return {"status":404, "resource": f"Couldn't find: {category}"}


    def getusersettings(self, id = None):
        with open(self.userstore) as f:
            data = json.loads(f.read())
        if not id:
            return {"status": 200, "resource": data}

        if id in data:
            return {"status": 200, "resource": data[id]}
        else:
            return {"status": 404, "resource": f"Couldn't find id {id}"}


    def setsettings(self, category, itemname, item, overwrite = False):
        # implement feature to append to list/dict, instead of overwrite
        with open(self.settingsfile) as f:
            data = json.loads(f.read())
        if category in data:
            if itemname in data[category]:
                if overwrite:
                    subitem = data[category][itemname]
                    if type(subitem) == list:
                        newitem = subitem + item
                        item = newitem
                    if type(subitem) == dict:
                        item.update(subitem)
            data[category][itemname] = item
            self.savefile(self.settingsfile, data)
            return {"status":201, "resource":f"Saved {itemname}"}
        else:
            data[category] = {}
            self.savefile(self.settingsfile, data)

            # run again
            self.setsettings(category, itemname, item)

    def setusersettings(self, newdata, id=None):
        with open(self.userstore) as f:
            userdata = json.loads(f.read())

        if id:
            id = str(id)
            olddict = userdata[id]
            olddict.update(newdata)
            
            userdata[id] = olddict
            self.savefile(self.userstore, userdata)
            return {"status": 201, "resource": userdata[id]}
        else:
            id = str(len(userdata) +1)
            userdata[id] = {}
            newdata["id"] = id # add id now
            self.savefile(self.userstore, userdata)
            res = self.setusersettings(newdata, id)["resource"]
            self.logger("creating new user..", "debug", "blue")
            return {"status": 201, "resource": res}

    def savefile(self, filename, data):
        with open(filename, "w") as f:
            f.write(json.dumps(data))

    def findtarget(self, search):
        search = str(search)
        finalnames = []
        with open("data/userstore.json", "r") as f:
            userdict = json.loads(f.read())

        for machine in userdict:
            name = machine
            capabilities = list(userdict[machine]["capabilities"])
            subscription = list(userdict[machine]["subscriptions"])
            devtype = userdict[machine]["devtype"]
            id = userdict[machine]["id"]
            if search == name:
                finalnames.append(machine)
            elif search in capabilities:
                finalnames.append(machine)
            elif search in subscription:
                finalnames.append(machine)
            elif search in devtype:
                finalnames.append(machine)
            elif search in str(id):
                finalnames.append(machine)
        if len(finalnames) > 0:
            return {"status": 200, "resource": finalnames}
        else:
            return {"status": 404, "resource": f"Couldn't find: {search}"}
