from flask import Flask, jsonify, request, render_template
from funcs import *
from flask_uploads import UploadSet, configure_uploads, AUDIO

app = Flask(__name__)

music = UploadSet('music', AUDIO)

app.config["UPLOADED_MUSIC_DEST"] = "static/audio"
configure_uploads(app, music)

@app.route('/sysinfo')
def sysinfo():
    return jsonify(get_sysinfo()), 200

@app.route('/upload', methods=["POST", "GET"])
def upload():
    if request.method == "POST" and 'audio' in request.files:
        filename = music.save(request.files['audio'])
        return filename
    # testing purposess only
    # return render_template("template.html")

if __name__ == "__main__":
    app.run(port=9000)