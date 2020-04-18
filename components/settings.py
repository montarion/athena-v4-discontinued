import os, json, redis
from time import sleep
from components.logger import logger as mainlogger

class settings:
    def __init__(self):
        self.tag = "settings"
        self.settingsfile = "data/settings.json"
        self.userstore = "data/userstore.json"

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def getsettings(self, category, item):
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


    def getusersettings(self, name):
        with open(self.userstore) as f:
            data = json.loads(f.read())

        if name in data:
            return {"status": 200, "resource": data[name]}
        else:
            return {"status": 404, "resource": f"Couldn't find {name}"}


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

    def setusersettings(self, name, newdata):
        with open(self.userstore) as f:
            userdata = json.loads(f.read())

        if name in userdata:
            olddict = userdata[name]
            olddict.update(newdata)
            userdata[name] = olddict
            self.savefile(self.userstore, userdata)
            return {"status": 201, "resource": userdata[name]}
        else:
            userdata[name] = {}
            id = len(userdata) +1
            newdata["id"] = id # add id now
            self.savefile(self.userstore, userdata)
            self.setusersettings(name, newdata)
            self.logger("creating new user..", "debug", "blue")
    def savefile(self, filename, data):
        with open(filename, "w") as f:
            f.write(json.dumps(data))

    def findtarget(self, search):
        # TODO: implement function to add elements to a user/machine
        finalnames = []
        with open(self.userstore) as f:
            userdict = json.loads(f.read())

        for machine in userdict:
            name = machine
            capabilities = userdict[machine]["capabilities"]
            subscription = userdict[machine]["subscriptions"]
            type = userdict[machine]["type"]
            if search == name:
                finalnames.append(machine)
            elif search in capabilities:
                finalnames.append(machine)
            elif search in subscription:
                finalnames.append(machine)
            elif search in type:
                finalnames.append(machine)
        if len(finalnames) > 0:
            return {"status": 200, "resource": finalnames}
        else:
            return {"status": 404, "resource": f"Couldn't find: {search}"}
