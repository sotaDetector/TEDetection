from flask import Blueprint, request
from tedService.tedRTCService.tedRTCServ import tedRTCSer

tedrtc_blp = Blueprint("tedRTCDispacher", __name__, url_prefix="/tedRTC")

tedRTCSer = tedRTCSer()



@tedrtc_blp.route("/createClient",methods=['POST'])
def createClient():
    jsonData = request.get_json()
    print("接收到参数",jsonData)
    return tedRTCSer.createClient(jsonData["roomId"])


@tedrtc_blp.route("/createSendOnlyClient",methods=['POST'])
def createMonitorClient():
    jsonData = request.get_json()
    print("接收到参数",jsonData)
    return tedRTCSer.createSendOnlyClient(jsonData["roomId"])

@tedrtc_blp.route("/createRecvOnlyClient",methods=['POST'])
def createRecvOnlyClient():
    jsonData = request.get_json()
    print("接收到参数",jsonData)
    return tedRTCSer.createRecvOnlyClient(jsonData["roomId"])