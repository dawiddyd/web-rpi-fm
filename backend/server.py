from flask import Flask, jsonify, request, render_template
from funcs import *
from flask_uploads import UploadSet, configure_uploads, AUDIO
from flask_cors import CORS
from tinytag import TinyTag
import subprocess
import signal
import datetime
import os

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

music = UploadSet('music', AUDIO)

app.config["UPLOADED_MUSIC_DEST"] = "static/audio"
app.config["JSON_AS_ASCII"] = False
configure_uploads(app, music)

pifm_proc = None

@app.route('/start', methods=["POST"])
def start():
    global pifm_proc
    file_name = request.form["file_name"]
    freq = request.form["freq"]
    radio_text = request.form["radio_text"]
    # m = subprocess.Popen("./pi_fm_adv --audio " + file_name + " --freq " + freq + " --rt " + radio_text)
    # m.wait()
    if pifm_proc and not pifm_proc.poll():
        print("Killing")
        # os.killpg(os.getpgid(pifm_proc.pid), signal.SIGTERM)
        subprocess.Popen("sudo killall pi_fm_adv", shell=True)
        print("Killed")
        pifm_proc = None

    cmd = "sox -t mp3 {} -t wav - | sudo ./pi_fm_adv --audio - --freq {} --rt {}".format(file_name, freq, radio_text) 
    print("Cmd: {}".format(cmd))
    pifm_proc = subprocess.Popen(cmd, shell=True, cwd="static/audio", preexec_fn=os.setsid)
    return jsonify(), 200

@app.route('/sysinfo')
def sysinfo():
    return jsonify(get_sysinfo()), 200

@app.route('/ls')
def file_list():
    payload = {}
    # p = subprocess.Popen("ls", stdout=subprocess.PIPE, shell=True, cwd="static/audio")
    # p.wait()
    # files = p.stdout.readlines()
    # files = [x.strip() for x in files]
    i = 0
    for r, d, f in os.walk("static/audio"):
        for f2 in f:
            try:
                file = f2
                f = TinyTag.get("static/audio/" + file, image=True)
                if not f.title:
                    f.title = file
                img_exists = os.path.isfile("static/img/" + file.split(".")[0] + ".png")
                if img_exists:
                    img_path = file.split(".")[0] + ".png"
                else:
                    img_path = None
                payload[i] = {
                    "filename": file,
                    "name": f.title,
                    "length": f.duration,
                    "author": f.artist,
                    "img": img_path
                }
                i += 1
            except:
                pass
    return jsonify(payload)
    
@app.route('/upload', methods=["POST"])
def upload():
    if request.method == "POST" and 'audio' in request.files:
        filename = music.save(request.files['audio'])
        f = TinyTag.get("static/audio/" + filename, image=True)
        image_data = f.get_image()
        if image_data:
            image_name = filename.split(".")[0]
            with file("static/img/" + image_name + ".png", 'wb') as x:
                x.write(image_data)
        return filename

if __name__ == "__main__":
    app.run(port=9000, host='0.0.0.0')

# p = subprocess.Popen("sox -t mp3 nighoffire.mp3 -t wav - | sudo ./pi_fm_adv --audio - --freq 88", stdout=subprocess.PIPE, shell=True, cwd="static/audio")
# p.wait() 