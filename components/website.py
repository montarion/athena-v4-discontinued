from flask import Flask, render_template
from flask_sockets import Sockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

try:
    from components.settings import settings
except:
    from settings import settings
import os, json, redis


class website:
    def __init__(self):
        self.app = Flask(__name__)
        self.sockets = Sockets(self.app)

    def messagehandler(self, ws, message):
            message = json.loads(message)

            category = message["category"]
            type = message["type"]
            data = message.get("data", {}) # optional
            metadata = message.get("metadata", {}) # optional

            if category == "anime":
                if type == "list":
                    preanilist = settings().getsettings("anime", "list")
                    if preanilist["status"] == 200:
                        anilist = preanilist["resource"]
                        finaldict = {"status": 200, "category": category, "type": type, "data":{"list":anilist}}
                        ws.send(json.dumps(finaldict))
                    else:
                        finaldict = {"status": 500, "category": category, "type": type}
                        ws.send(json.dumps(finaldict))

    def runserver(self):

        @self.sockets.route('/')
        def socket(ws):
            try:
                while not ws.closed:
                    message = ws.receive()
                    print(f"Message received: {message}")
                    self.messagehandler(ws, message)
                    ws.send(message)
            except webSocketError:
                print("lost connection!")
            except Exception as e:
                print("ERROR!")
                print(e.__class__.__name__)

        @self.app.route('/')
        def hello():
            return render_template("index.html")


        server = pywsgi.WSGIServer(('0.0.0.0', 8080), self.app, handler_class=WebSocketHandler)
        server.serve_forever()

if __name__ == "__main__":
    print("Starting as standalone")
    website().runserver()
