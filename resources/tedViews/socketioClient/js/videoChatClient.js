
var socket = io.connect();


function joinRoom(){

    socket.emit('join', '123');
}



function sendMessage(roomId,data){
    socket.emit('message',roomId,data);
}


function conn() {
    socket.on('joined', (room) => {
        console.log("server return tag:" + room);
    })
}

conn();