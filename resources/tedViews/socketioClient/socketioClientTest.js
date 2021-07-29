var socketioClient=io.connect("http://localhost:3660")

function joinRoom(){
    socketioClient.emit('join',{
        "roomId":$("#roomId").val(),
        "userId":"12345",
        "data":{}
    })
}

socketioClient.on("joined",function(data){

    console.log("joined successfully");
    console.log(data);


})