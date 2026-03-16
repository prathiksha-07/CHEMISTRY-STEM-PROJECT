from flask import Flask, jsonify
import serial
import json

app = Flask(__name__)

# Change COM port
ser = serial.Serial('COM4', 115200)  # Change if needed

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