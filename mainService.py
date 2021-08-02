from flask import Flask
import threading

from tedService.mediaPlayerService.mediaPlayerDispacher import media_Player_blp
from tedService.tedRTCService.tedRTCDispacher import tedrtc_blp

app = Flask(__name__, static_folder='resources/tedViews', static_url_path='/')

app.register_blueprint(media_Player_blp)
app.register_blueprint(tedrtc_blp)

app.run(host='0.0.0.0',
        port=8001)
