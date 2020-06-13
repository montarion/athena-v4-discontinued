import os, redis, json, schedule
from time import sleep
from fuzzywuzzy import process 
from components.logger import logger as mainlogger
from components.anime import anime
from components.weather import weather
import components.helpers.Q as Q

class Modules:
    def __init__(self):
        self.q = Q.baseQueue
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.tag = "modules"

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def standard(self):
        #sleep(10)
        schedule.every(20).seconds.do(anime().getshows)
        schedule.every(5).seconds.do(weather().getcurrentweather)
        while True:
            #self.logger("Running anime!")
            #anime().getshows()
            #self.logger("Running weather!")
            #weather().getcurrentweather()
            #Event().anime()
            #sleep(20)
            schedule.run_pending()
            sleep(5)
    def getlocation(self):
        pass


    def fuzzysearch(self, target, options, searchtype = "highest", include_score=False):
        # use for letting users search for stuff
        if searchtype == "highest":
            searchres = process.extractOne(target, options)
            if not include_score:
                return searchres[0]
            else:
                return searchres
        elif searchtype == "best":
            searchres = process.extractBests(target, options, score_cutoff=80, limit=3)
            if not include_score:
                reslist = [x[0] for x in searchres]
                return reslist
            else:
                return searchres
