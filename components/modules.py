import os, redis, json
from time import sleep

from components.logger import logger as mainlogger
from components.anime import anime
from components.events import Event
class Modules:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.tag = "modules"

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def standard(self):
        sleep(10)
        while True:
            self.logger("Running anime!")
            anime().getshows()

            Event().anime()
            sleep(20)
