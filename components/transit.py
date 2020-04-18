import requests, json, os, redis, datetime
from time import sleep, time

from components.settings import settings
from components.logger import logger as mainlogger
from components.helpers.oauth import oauth

class transit:
    def __init__(self):
        self.tag = "transit"

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def getauthentication(self):
        headers = {}
        preapicreds = settings().getsettings("credentials", "hereapi")
        if preapicreds["status"] == 200:
            apicreds = preapicreds["resource"]
            
            if "access_token" in apicreds:
                expirationdate = apicreds["expires_at"]
                if int(int(time())) < expirationdate: # token has expired, so ask for a new one
                    accesstoken = apicreds["access_token"]
                else:
                    id = apicreds["key_id"]
                    secret = apicreds["key_secret"]
                    accesstoken = oauth().get_token(id, secret)
            else: # apparently no token exists yet
                id = apicreds["key_id"]
                secret = apicreds["key_secret"]
                accesstoken = oauth().get_token(id, secret)
        else: # no settings dict exists, warn user and make them fill it in.
            return {"status": 404, "resource": "Please link with the HERE location services API."}

        headers["Authorization"] = "Bearer " + accesstoken
        return headers

    def getbusstops(self, coordinates, range = 500):
        lat, lon = coordinates
        latlon = f"{lat},{lon}"
        url = "https://transit.hereapi.com/v8/stations"
        headers = self.getauthentication() # returns "headers" dictionary
        params = {
                "in": latlon,
                "r": range,
                "return": "transport"
                }


        result = requests.get(url=url, params= params, headers=headers)
        return result.json()

    def getnextdeparturesatstop(self, busstopid = None):
        if not busstopid:
            prebusstop = settings().getsettings("Personalia", "homebusid")
            if prebusstop["status"] == 200:
                 busstopid = prebusstop["resource"]
            else:
                # alert the user to ask for busstop id
                pass
        url = "https://transit.hereapi.com/v8/departures"
        headers = self.getauthentication()
        params = {
                "ids":busstopid
                }

        result = requests.get(url=url, params= params, headers=headers)
        return result.json()


