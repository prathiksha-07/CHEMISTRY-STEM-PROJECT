from flask import Flask, jsonify
from flask_cors import CORS
import serial
import threading
import time
import json

app = Flask(__name__)
CORS(app)

SERIAL_PORT = 'COM7'
BAUD_RATE = 115200

sensor_data = {
    "ph": 0.0,
    "turbidity": 0.0,
    "tds": 0.0,
    "temperature": 0.0
}

ser = None


def init_serial():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Serial opened on {SERIAL_PORT} @ {BAUD_RATE}")
    except Exception as e:
        print(f"Serial init error: {e}")
        ser = None


def read_serial_loop():
    global sensor_data, ser
    while True:
        if ser is None:
            time.sleep(1)
            continue
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    sensor_data.update(data)
            except Exception:
                pass
        except Exception:
            pass


@app.route('/')
def home():
    return "Backend running. Use /data"


@app.route('/status')
def status():
    return {
        "status": "running",
        "has_serial": ser is not None
    }


@app.route('/data')
def get_data():
    return jsonify(sensor_data)


if __name__ == '__main__':
    init_serial()
    thread = threading.Thread(target=read_serial_loop, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
