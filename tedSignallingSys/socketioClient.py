import socketio

sioClient=socketio.Client()



sioClient.connect(url='http://121.40.99.127:3660/')

sioClient.emit("message","hello i am python client")

sioClient.wait()