
'''from flask import Flask, jsonify
import serial
import json

app = Flask(__name__)# Change COM port
ser = serial.Serial('COM7', 9600)  # Change if needed

sensor_data = {
    "ph": 0,
    "turbidity": 0,
    "tds": 0,
    "temperature": 0
}

@app.route('/data')
def get_data():
    global sensor_data
    
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        try:
            sensor_data = json.loads(line)
        except:
            pass

    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(port=5000)
@app.route('/data')
def get_data():
    global sensor_data
    
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        try:
            sensor_data = json.loads(line)
        except:
            pass

    return jsonify(sensor_data)

if __name__ == '__main__':'''

''' original code
from flask import Flask, jsonify
import time
import serial
import json

app = Flask(__name__)

sensor_data = {
    "ph": 0,
    "turbidity": 0,
    "tds": 0,
    "temperature": 0
}

def get_serial():
    #return serial.Serial('COM7', 9600, timeout=1)
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)   # 🔥 MUST
    return ser

@app.route('/')
def home():
    return "Backend is running! Go to /data"
@app.route('/status')
def status():
    return {"status": "running"}
@app.route('/data')
def get_data():
    global sensor_data
    
    try:
        ser = get_serial()

        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("Received:", line) 
            try:
                sensor_data = json.loads(line)
            except:
                pass

        ser.close()

    except Exception as e:
        print("Serial error:", e)

    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(port=5000, debug=False)'''


'''              // thread from flask import Flask, jsonify
import serial
import json
import threading
import time

app = Flask(__name__)

sensor_data = {"ph":0,"tds":0,"temperature":0,"turbidity":0}

# 🔌 Serial setup
ser = serial.Serial('COM7', 9600)
time.sleep(2)

# 🔁 Background thread (IMPORTANT)
def read_serial():
    global sensor_data
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            print("RAW:", line)

            data = json.loads(line)
            sensor_data = data   # ✅ update here

        except Exception as e:
            print("Error:", e)

# ▶ start thread
thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

# 🌐 API
@app.route('/data')
def get_data():
    return jsonify(sensor_data)

# 🚀 Run
if __name__ == '__main__':
    app.run(debug=True)'''
#####################
'''from flask import Flask, jsonify
import serial
import json

app = Flask(__name__)

sensor_data = {
    "ph": 0,
    "turbidity": 0,
    "tds": 0,
    "temperature": 0
}

def get_serial():
    return serial.Serial('COM7', 9600, timeout=1)

@app.route('/data')
def get_data():
    global sensor_data
    
    try:
        ser = get_serial()
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("RAW Received:", line)

            # JSON validate
            if line.startswith("{") and line.endswith("}"):
                try:
                    sensor_data = json.loads(line)
                    print("Parsed:", sensor_data)
                except json.JSONDecodeError as e:
                    print("JSON Error:", e)

        ser.close()

    except Exception as e:
        print("Serial error:", e)

    return jsonify(sensor_data)

@app.route('/')
def home():
    return "Backend is running! Go to /data"

if __name__ == '__main__':
    app.run(port=5000, debug=False)'''


'''from flask import Flask, jsonify
import serial
import json

app = Flask(__name__)

# 1-time serial open
ser = serial.Serial('COM7', 9600, timeout=1)

sensor_data = {
    "ph": 0,
    "turbidity": 0,
    "tds": 0,
    "temperature": 0
}

@app.route('/')
def home():
    return "Backend is running! Go to /data"

@app.route('/data')
def get_data():
    global sensor_data
    try:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("RAW Received:", line)
            # validate JSON
            if line.startswith("{") and line.endswith("}"):
                try:
                    sensor_data = json.loads(line)
                    print("Parsed:", sensor_data)
                except json.JSONDecodeError as e:
                    print("JSON Error:", e)
    except Exception as e:
        print("Serial error:", e)

    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(port=5000, debug=False)'''


from flask import Flask, jsonify
from flask_cors import CORS
import serial
import time
import json

app = Flask(__name__)
CORS(app)

ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

sensor_data = {
    "ph": 0,
    "turbidity": 0,
    "tds": 0,
    "temperature": 0
}

@app.route('/')
def home():
    return "Server running"

@app.route('/data')
def get_data():
    global sensor_data

    try:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("Received:", line)

            try:
                sensor_data = json.loads(line)
            except:
                pass

    except Exception as e:
        print("Error:", e)

    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(port=5000)