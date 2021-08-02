from flask import Blueprint, request
from tedService.tedRTCService.tedRTCServ import tedRTCSer

tedrtc_blp = Blueprint("tedRTCDispacher", __name__, url_prefix="/tedRTC")

tedRTCSer = tedRTCSer()



@tedrtc_blp.route("/createClient",methods=['POST'])
def createClient():
    jsonData = request.get_json()
    print("接收到参数",jsonData)
    return tedRTCSer.createClient(jsonData["roomId"])