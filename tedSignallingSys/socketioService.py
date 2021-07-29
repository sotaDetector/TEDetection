from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from tedSignallingSys.sigSys.sigServiceCore import sigServiceCore

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app, cors_allowed_origins="*")

sigService = sigServiceCore()


@socketio.on('join')
def join(data):
    sigService.join(data)


@socketio.on("message")
def onMessage(data):
    print("receive message", data)


@socketio.on('leave')
def leave(roomId):
    pass


def runScoketIo():
    socketio.run(app, host="0.0.0.0", port=3660)
    print("start socket io successfully...")


if __name__ == '__main__':
    runScoketIo()
