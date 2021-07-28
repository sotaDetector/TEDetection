from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})

def runScoketIo():
    print("start socket io begin...")
    socketio.run(app)
    print("start socket io successfully...")
if __name__ == '__main__':
    runScoketIo()