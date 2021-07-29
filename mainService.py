from flask import Flask
import threading

from tedService.mediaPlayer.mediaPlayerDispacher import media_Player_blp
from tedSignallingSys.socketioService import  runScoketIo

app = Flask(__name__, static_folder='resources/ted', static_url_path='/')

app.register_blueprint(media_Player_blp)

#start signalling system
threading.Thread(target=runScoketIo).start()

app.run(host='0.0.0.0',
        port=8001)
