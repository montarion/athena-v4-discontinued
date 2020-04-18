from Flask import flask, render_template
from flask_sockets import sockets
import os, json, redis


class website:
    def __init__(self):
        self.app = Flask(__name__)
        self.sockets = Sockets(self.app)

    def runserver(self):

        @sockets.route('/echo')
        def echo_socket(ws):
            while not ws.closed:
                message = ws.receive()
                ws.send(message)

        @sockets.route("/anime")
        def anime(ws):
            while not ws.closed:
                message = ws.receive()

        @app.route('/')
        def hello():
            return render_template("index.html")

