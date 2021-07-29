import socketio

sioClient=socketio.Client()



sioClient.connect(url='http://192.168.1.7:3660/')




def joinedRoom(data):
    print("...........")
    print(data)

def otherJoined(data):
    print("************")
    print(data)

sioClient.on("joined",joinedRoom)

sioClient.on("otherJoined",otherJoined)

sioClient.emit("join",{
    "roomId":"123",
    "userId":"test",
    "data":{}
})

sioClient.wait()