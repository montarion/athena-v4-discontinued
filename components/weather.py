import os, requests, json, redis, re, time, traceback

from components.logger import logger as mainlogger
from components.settings import settings
from components.events import Event

class weather:
    def __init__(self):
        self.tag = "weather"
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.refreshtime = 30 #change 30 to  after testing # seconds # TODO: make this a setting

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def getcurrentweather(self):
        self.logger("CHANGE WEATHER INTERVAL", "alert", "red")
        prelocation = settings().getsettings("personalia", "location")["resource"]

        if "coords" not in prelocation:
            self.logger("Unable to find coordinates","alert", "red")
            # ask for location(TODO: modules > getlocation?)
            # then try again
            #self.getforecast()

        lat, lon = prelocation["coords"]
        if "apikey" not in prelocation:
            self.logger("Weather api key not found.", "alert", "red")
            # run setup(TODO) again, explicitely asking for the weather api key.
            # then try again
            #self.getforecast()

        title = prelocation["city"] # if coords are in, city name will also be in
        apikey = prelocation["apikey"]

        baseurl = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={apikey}&units=metric"

        #TODO try-catch this HTTP request
        res = requests.get(baseurl).json()
        if len(res.keys()) == 2:
            # error occured, read message
            self.logger(f"Error: {res['cod']}", "alert", "red")
            self.logger(f"Message: {res['message']}", "alert", "red") 

        try:
            timezone = res["timezone"]
            # maybe write to file

            # current weather
            curdict = {}
            cur = res["current"]
            dt = int(time.time()) # time of request, unix, utc
            temp = cur["temp"]
            sunrise = cur["sunrise"]
            sunset = cur["sunset"]
            clouds = cur["clouds"] # cloudiness in %
            rain = cur.get("rain", None)
            windspeed = cur["wind_speed"]
            icon = cur["weather"][0]["icon"]
            iconbase = "http://openweathermap.org/img/wn/"
            iconurl = iconbase + icon + "@2x.png"
            curdict = {"location": title, "time": dt, "temp":temp, "rain":rain, "sunrise":sunrise, "sunset":sunset, "clouds":clouds, "windspeed":windspeed, "iconurl":iconurl}
            # cache this to file, maybe?
            preoldweather = settings().getsettings("weather", "current")
            if preoldweather["status"] == 200:
                oldweather = preoldweather["resource"]
                oldtime = oldweather["time"]
                timediff = dt - oldtime
                if timediff > self.refreshtime:
                    settings().setsettings("weather", "current", curdict)
                    Event().weather(curdict)
                
            else:
                settings().setsettings("weather", "current", curdict)
                Event().weather(curdict)
            return {"status":200, "resource":curdict}
        except Exception as e:
            #self.logger(e, "alert", "red")
            traceback.print_exc()
            return {"status":503, "resource": "something went wrong."}
