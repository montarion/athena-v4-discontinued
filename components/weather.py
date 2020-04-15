import os, requests, json, redis, re

from components.logger import logger as mainlogger
from components.settings import settings

class weather:
    def __init__(self):
        self.tag = "weather"
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def getforecast(self):
        prelocation = settings().getsettings("personalia", "location")["resource"]
        if "coords" not in prelocation:
            self.logger("Unable to find coordinates")
            # ask for location(TODO: modules > getlocation?)
            # then try again
            #self.getforecast()

        lat, lon = prelocation["coords"]
        if "apikey" not in prelocation:
            self.logger("Weather api key not found.")
            # run setup(TODO) again, explicitely asking for the weather api key.
            # then try again
            #self.getforecast()

        title = prelocation["name"]
        apikey = prelocation["apikey"]

        baseurl = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={apikey}&units=metric"
        res = requests.get(baseurl).json()
        self.logger(res.keys())
        try:
            timezone = res["timezone"]
            # maybe write to file

            # current weather
            curdict = {}
            cur = res["current"]
            dt = cur["dt"] # time of request, unix, utc
            temp = cur["temp"]
            sunrise = cur["sunrise"]
            sunset = cur["sunset"]
            clouds = cur["clouds"] # cloudiness in %
            rain = cur.get("rain", None)
            windspeed = cur["wind_speed"]
            icon = cur["weather"][0]["icon"]

            curdict = {"time": dt, "temp":temp, "rain":rain, "sunrise":sunrise, "sunset":sunset, "clouds":clouds, "windspeed":windspeed, "icon":icon}
            # cache this to file, maybe?

            return {"status":200, "resource":curdict}
        except Exception as e:
            self.logger(e, "alert", "red")
            return {"status":503, "resource": "something went wrong."}
