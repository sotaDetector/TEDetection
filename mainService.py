from flask import Flask

from tedService.mediaPlayer.mediaPlayerDispacher import media_Player_blp

app = Flask(__name__, static_folder='resources/ted', static_url_path='/')

app.register_blueprint(media_Player_blp)


app.run(host='0.0.0.0',
        port=8001)