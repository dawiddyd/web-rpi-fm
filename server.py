from flask import Flask, jsonify, request, render_template, send_from_directory
from funcs import *
from flask_uploads import UploadSet, configure_uploads, AUDIO
from flask_cors import CORS
from tinytag import TinyTag
import subprocess
import signal
import datetime
import os
import time

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

music = UploadSet('music', AUDIO)

app.config["UPLOADED_MUSIC_DEST"] = "static/audio"
app.config["JSON_AS_ASCII"] = False
configure_uploads(app, music)

pifm_proc = None
playing_file = None
start_time = 0
streaming = False
radio_text = ""

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

@app.route('/start', methods=["POST"])
def start():
    global pifm_proc
    global playing_file
    global start_time
    global streaming

    streaming = False

    json = request.get_json()
    file_name = json["file_name"]
    freq = json["freq"]
    file = TinyTag.get("static/audio/" + file_name, image=True)
    radio_text = removeNonAscii(file.title + " " + file.artist)

    # m = subprocess.Popen("./pifmrds -audio " + file_name + " -freq " + freq + " -rt " + radio_text)
    # m.wait()
    if pifm_proc and not pifm_proc.poll():
        print("Killing")
        # os.killpg(os.getpgid(pifm_proc.pid), signal.SIGTERM)
        subprocess.Popen("sudo killall pifmrds", shell=True)
        print("Killed")
        pifm_proc = None

    cmd = "sox -t mp3 {} -t wav - | sudo ./pifmrds -audio - -freq {} -rt '{}'".format(file_name, freq, radio_text) 
    print("Cmd: {}".format(cmd))
    pifm_proc = subprocess.Popen(cmd, shell=True, cwd="static/audio", preexec_fn=os.setsid)

    playing_file = file_name
    start_time = time.time()

    return jsonify(), 200

@app.route('/starturl', methods=["POST"])
def starturl():
    global pifm_proc
    global playing_file
    global start_time
    global streaming
    global radio_text

    streaming = True

    json = request.get_json()
    file_name = json["file_name"]
    freq = json["freq"]
    radio_text = json["radio_text"]
    # radio_text = "web-rpi-fm"
    # m = subprocess.Popen("./pifmrds -audio " + file_name + " -freq " + freq + " -rt " + radio_text)
    # m.wait()
    if pifm_proc and not pifm_proc.poll():
        print("Killing")
        # os.killpg(os.getpgid(pifm_proc.pid), signal.SIGTERM)
        subprocess.Popen("sudo killall pifmrds", shell=True)
        print("Killed")
        pifm_proc = None

    cmd = "sox -t mp3 {} -t wav - | sudo ./pifmrds -audio - -freq {} -rt {}".format(file_name, freq, radio_text) 
    print("Cmd: {}".format(cmd))
    pifm_proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

    playing_file = file_name
    start_time = time.time()

    return jsonify(), 200

@app.route('/<path:path>')
def send_static(path):
    if not os.path.isfile("static/" + path):
        return app.send_static_file('index.html')    
    return send_from_directory('static', path)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/stop', methods=["POST"])
def stop():
    global pifm_proc

    if pifm_proc and not pifm_proc.poll():
        print("Killing")
        # os.killpg(os.getpgid(pifm_proc.pid), signal.SIGTERM)
        subprocess.Popen("sudo killall pifmrds", shell=True)
        print("Killed")
        pifm_proc = None

    return jsonify(), 200

@app.route('/status', methods=["GET"])
def status():
    global pifm_proc
    global playing_file
    global start_time
    global streaming
    global radio_text

    running = pifm_proc and not pifm_proc.poll()

    if not running:
        return jsonify({
            "running": False,
        }), 200

    if streaming:
        return jsonify({
            "running": True,
            "filename": playing_file,
            "name": radio_text,
            "time_elapsed": time.time() - start_time,
        }), 200
    
    file = playing_file
    f = TinyTag.get("static/audio/" + file, image=True)
    if not f.title:
        f.title = file

    img_path = None
    
    img_exists = os.path.isfile("static/img/" + file.split(".")[0] + ".png")
    if img_exists:
        img_path = file.split(".")[0] + ".png"

    return jsonify({
        "running": True,
        "filename": file,
        "name": f.title,
        "length": f.duration,
        "author": f.artist,
        "img": img_path,
        "time_elapsed": time.time() - start_time,
    }), 200

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

@app.route('/delete', methods=["POST"])
def delete():
    if request.method == "POST":
        json = request.get_json()
        filename = json["filename"]
        os.remove("static/audio/" + filename)
        try:
            image_name = filename.split(".")[0]
            os.remove("static/audio/" + image_name + ".png")
        except:
            pass

        return jsonify(), 200

if __name__ == "__main__":
    subprocess.Popen("sudo killall pifmrds", shell=True)
    app.run(port=9000, host='0.0.0.0')

# p = subprocess.Popen("sox -t mp3 nighoffire.mp3 -t wav - | sudo ./pi_fm_adv --audio - --freq 88", stdout=subprocess.PIPE, shell=True, cwd="static/audio")
# p.wait()
