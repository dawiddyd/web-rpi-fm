from flask import Flask, jsonify
from funcs import *

app = Flask(__name__)

@app.route('/sysinfo')
def sysinfo():
    return jsonify(get_sysinfo()), 200

if __name__ == "__main__":
    app.run(port=9000)