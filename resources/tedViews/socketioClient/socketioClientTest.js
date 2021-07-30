//------------------define constant start----------------
var socketioClient=null;
var pc=null;
pcState=null;

var localStream=null;
var remoteStream=null;

var localVideo = document.querySelector('video#localVideo');
var remoteVideo = document.querySelector('video#remoteVideo');


let SING_JOINED = 'joined'
let SING_OTHER_JOINED = 'otherJoined'
let SING_LEAVED = 'leaved'
let SING_OTHER_LEAVED = 'otherLeaved'
let SING_MESSAGE = "message"


var pcConfig={
    'iceServers':[
        {
            'urls': 'turn:iclockmaker.com:3478',
            'credential': "158246",
            'username': "tvs"
        }
    ]
}





//------------------define constant end----------------

function createSocketClient(){
    console.log("IMSTEP[2]-create socketio client start");
    socketioClient=io.connect("http://localhost:3660")
    console.log("IMSTEP[2]-create socketio client end");
}

function sendData(eventType,data){

    socketioClient.emit(eventType,{
        "roomId":$("#roomId").val(),
        "userId":"12345",
        "data":data
    })

}

function joinRoom(){
    console.log("IMSTEP[3]-join room start");
    sendData('join',{});
}

function sendMsg(){
    sendData('message',$("#messageContent").val());
}

function leaveRoom() {
   sendData('leave', {});
}

function getRemoteStream(remoteStreamData){
    remoteStream=remoteStreamData.stream[0];
    remoteVideo.srcObject=remoteStream;
}

function createPeerConnection(){
    //create peer connection
    if(pc){
        console.log(" the rtcPeerconnection has bean created");
        return;
    }
    console.log("IMSTEP[4]-create RTCPeerconnection start");
    pc=new RTCPeerConnection(pcConfig);

    pc.onicecandidate=(e)=>{
        if(e.candidate){
            sendData("message",{
                type: 'candidate',
                label:event.candidate.sdpMLineIndex,
                id:event.candidate.sdpMid,
                candidate: event.candidate.candidate
             })
        }
    }
    pc.ontrack=getRemoteStream;
   console.log("IMSTEP[4]-create RTCPeerconnection end");

}

function createOffer(isReceiveAudio,isReceiveVideo){
    console.log("IMSTEP[7]-create offer start");
    var offerOptions={
        offerToReceiveAudio:isReceiveAudio,
        offerToReceiveVideo:isReceiveVideo
    }
    pc.createOffer(offerOptions)
        .then(function(desc){
            //set local description
            pc.setLocalDescription(desc);
            //send sdp offer
            sendData("message",desc);
            console.log("IMSTEP[7]-create offer end");
        }).catch(function(error){
            console.log("faield to create offer");
        })

}

function bindTrack(){
    console.log("IMSTEP[5]-bind tracks into RTCPeerConnection start");
    if(pc===null || pc===undefined){
        console.log("pc is null");
        return;
    }
     if(localStream===null || localStream===undefined){
        console.log("localStream is null");
        return;
    }
     //add all track into peer connection
    localStream.getTracks().forEach((track)=>{
        pc.addTrack(track,localStream);
    });
     console.log("IMSTEP[5]-bind tracks into RTCPeerConnection finished");
}

function getUserMediaStream(){
    if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
        console.log("the getUserMedia is not supported");
        return;
    }
    console.log("IMSTEP[1]-set local user media start");
    var constraints={
        video:{
            width:640,
            height:480
        },
        audio:{
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
        }
    }
    navigator.mediaDevices.getUserMedia(constraints)
        .then((streams)=>{
            if(localStream){
                streams.getAudioTracks().forEach((track)=>{
                    localStream.addTrack(track);
                    streams.removeTrack(track);
                });
            }else{
                localStream = streams;
            }
            localVideo.srcObject=localStream;
            console.log("IMSTEP[1]-set local user media end");
            //在成功获取到本地媒体之后再创建连接，否则pc绑定本地媒体资源可能会失败。
            // 而且如果获取本体媒体失败，也没有必要进行后续操作
            createSocketClient();
            //监听socketio信息
            initSocketMsgListener();
            //3.加入房间
            joinRoom();
        })
        .catch((e)=>{
            console.log("cat not get user media stream");
            console.log(e);
        });



}

function initSocketMsgListener(){

    console.log("init socket message listener");
    socketioClient.on(SING_JOINED,(data)=>{

        console.log("IMSTEP[3]-join room end");
        console.log(data);

        createPeerConnection();
        bindTrack();

    });

    socketioClient.on(SING_OTHER_JOINED,(data)=>{
        console.log("IMSTEP[6]~another client up line");
        createOffer(1,1);
    });

    socketioClient.on(SING_LEAVED,(data)=>{

    });

    socketioClient.on(SING_OTHER_LEAVED,(data)=>{

    });

    socketioClient.on(SING_MESSAGE,(data)=>{

    });

}


function start(){
    //1.获取本地媒体 如果获取不到媒体，就无需建立连接了，所以放第一步
    getUserMediaStream();

}