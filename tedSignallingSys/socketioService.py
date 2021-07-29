from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app,cors_allowed_origins="*")


@socketio.on("message")
def onMessage(message):
    print("receive message",message)

def runScoketIo():
    print("start socket io begin...")
    socketio.run(app,host="0.0.0.0",port=3660)
    print("start socket io successfully...")

if __name__ == '__main__':
    runScoketIo()