## Class to get oauth 2.0 bearer token for the here api.
## followed: https://developer.here.com/blog/requesting-here-oauth-bearer-token-using-python

import requests, time, urllib.parse, hmac, hashlib, binascii, datetime
from base64 import b64encode

from components.logger import logger as mainlogger
from components.settings import settings

class oauth:

    def __init__(self, grant_type = "client_credentials",signature_method = "HMAC-SHA256", oauth_version = "1.0", url = "https://account.api.here.com/oauth2/token"):
        self.tag = "oath"
        self.nonce = str(int(time.time()*1000))

        # make it usable for other oauth 2.0 requests
        self.oauth_grant_type = grant_type
        self.oauth_signature_method = signature_method
        self.oauth_version = oauth_version # for the here api, that has to be 1.0
        self.oauth_url = url
        

    def logger(self, msg, type="info", colour="none"):
        mainlogger().logger(self.tag, msg, type, colour)

    def create_signature(self, secret_key, signature_base_string):
        encoded_string = signature_base_string.encode()
        encoded_key = secret_key.encode()
        temp = hmac.new(encoded_key, encoded_string, hashlib.sha256).hexdigest()
        byte_array = b64encode(binascii.unhexlify(temp))
        return byte_array.decode()

    # concatenate the six oauth parameters, plus the request parameters from above, sorted alphabetically by the key and$
    def create_parameter_string(self):
        parameter_string = ''
        parameter_string = parameter_string + 'grant_type=' + self.oauth_grant_type
        parameter_string = parameter_string + '&oauth_consumer_key=' + self.oauth_consumer_key
        parameter_string = parameter_string + '&oauth_nonce=' + self.oauth_nonce
        parameter_string = parameter_string + '&oauth_signature_method=' + self.oauth_signature_method
        parameter_string = parameter_string + '&oauth_timestamp=' + self.oauth_timestamp
        parameter_string = parameter_string + '&oauth_version=' + self.oauth_version
        return parameter_string

    def get_token(self, consumer_key, access_key_secret):
        self.oauth_consumer_key = consumer_key
        self.access_key_secret = access_key_secret

        self.oauth_nonce = str(int(time.time()*1000))
        self.oauth_timestamp = str(int(time.time()))
        parameter_string = self.create_parameter_string()

        tokendict = self.request_token( parameter_string, self.oauth_url)
        accesstoken = tokendict["access_token"]
        expirationdate = int(time.time()) + int(tokendict["expires_in"])

        creddict = {}
        creddict["access_token"] = accesstoken
        creddict["expires_at"] = expirationdate
        
        settings().setsettings("credentials", "hereapi", creddict)
        return accesstoken

    def request_token(self, parameter_string, url):
        encoded_parameter_string = urllib.parse.quote(parameter_string, safe='')
        encoded_base_string = 'POST' + '&' + urllib.parse.quote(url, safe='')
        encoded_base_string = encoded_base_string + '&' + encoded_parameter_string

        # create the signing key
        signing_key = self.access_key_secret + '&'

        oauth_signature = self.create_signature(signing_key, encoded_base_string)
        encoded_oauth_signature = urllib.parse.quote(oauth_signature, safe='')

        #---------------------Requesting Token---------------------
        body = {'grant_type' : '{}'.format(self.oauth_grant_type)}

        headers = {
                'Content-Type' : 'application/x-www-form-urlencoded',
                'Authorization' : 'OAuth oauth_consumer_key="{0}",oauth_nonce="{1}",oauth_signature="{2}",oauth_signature_method="HMAC-SHA256",oauth_timestamp="{3}",oauth_version="1.0"'.format(self.oauth_consumer_key,self.oauth_nonce,encoded_oauth_signature,self.oauth_timestamp)
                }

        response = requests.post(url, data=body, headers=headers)

        return response.json()
