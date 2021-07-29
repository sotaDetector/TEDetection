var socketioClient=io.connect("http://localhost:3660")

function sendMsg(){
    socketioClient.emit('message',"hello")
}
