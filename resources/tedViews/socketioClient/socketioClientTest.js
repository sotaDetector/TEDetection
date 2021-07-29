var socketioClient=io.connect("http://localhost:3660/")

socketioClient.emit('message',"hello")
