from flask import Flask, render_template
from flask_sockets import Sockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

import os, json, redis


class website:
    def __init__(self):
        self.app = Flask(__name__)
        self.sockets = Sockets(self.app)
    def runserver(self):

        @self.sockets.route('/')
        def socket(ws):
            try:
                while not ws.closed:
                    message = ws.receive()
                    print(f"Message received: {message}")
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
