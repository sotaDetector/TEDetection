from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app,cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on("message")
def onMessage(message):
    print("receive message",message)

def runScoketIo():
    print("start socket io begin...")
    socketio.run(app,port=3660)
    print("start socket io successfully...")

if __name__ == '__main__':
    runScoketIo()