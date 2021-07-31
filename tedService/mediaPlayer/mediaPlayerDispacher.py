from flask import request, Blueprint, Response

from common.configPraserUtils import configUtils
from tedService.mediaPlayer.mediaPlayerService import mediaPlayerService

media_Player_blp = Blueprint("mediaPlayerDispacher", __name__, url_prefix="/mediaPlayer")
mediaPlayerSer = mediaPlayerService()


@media_Player_blp.route("/liveStreamPlayer")
def liveStreamPlayer():
    mediaSourceId = request.args.get("mediaSourceId")
    return Response(mediaPlayerSer.genFramesFromLiveStream(mediaSourceId),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
