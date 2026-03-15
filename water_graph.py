'''import serial
import matplotlib.pyplot as plt

# change COM port according to your system
ser = serial.Serial('COM7', 9600)

ph_list = []
tds_list = []
temp_list = []
turb_list = []

count = 0

while count < 10:   # collect 10 samples
    line = ser.readline().decode().strip()

    data = line.split(",")

    ph = float(data[0].split(":")[1])
    tds = float(data[1].split(":")[1])
    temp = float(data[2].split(":")[1])
    turb = float(data[3].split(":")[1])

    ph_list.append(ph)
    tds_list.append(tds)
    temp_list.append(temp)
    turb_list.append(turb)

    print("pH:", ph, "TDS:", tds, "Temp:", temp, "Turb:", turb)

    count += 1


# Graphs
plt.figure()
plt.plot(ph_list)
plt.title("pH Graph")
plt.xlabel("Samples")
plt.ylabel("pH Value")
plt.show()

plt.figure()
plt.plot(tds_list)
plt.title("TDS Graph")
plt.xlabel("Samples")
plt.ylabel("ppm")
plt.show()

plt.figure()
plt.plot(temp_list)
plt.title("Temperature Graph")
plt.xlabel("Samples")
plt.ylabel("°C")
plt.show()

plt.figure()
plt.plot(turb_list)
plt.title("Turbidity Graph")
plt.xlabel("Samples")
plt.ylabel("NTU")
plt.show()'''
# dummy graph
import serial
import matplotlib.pyplot as plt

# -----------------------------
# 1. Setup Serial (Change COM port)
# -----------------------------
# Arduino dummy values send பண்ணும் serial port-க்கு match பண்ணுங்க
ser = serial.Serial('COM7', 9600,timeout = 1)

# -----------------------------
# 2. Safe / Medium / Unsafe Ranges
# -----------------------------
safe_ranges = {"ph": (6.5, 8.5), "tds": (0, 500), "temp": (0, 35), "turb": (0, 5)}
medium_ranges = {"ph": (6.0, 6.5), "tds": (500, 700), "temp": (35, 40), "turb": (5, 10)}
param_names = ["ph", "tds", "temp", "turb"]

# -----------------------------
# 3. Classification Functions
# -----------------------------
def classify(value, param):
    safe = safe_ranges[param]
    medium = medium_ranges[param]
    if safe[0] <= value <= safe[1]:
        return "SAFE"
    elif medium[0] <= value <= medium[1]:
        return "MEDIUM"
    else:
        return "UNSAFE"

def get_color(status):
    if status == "SAFE":
        return "green"
    elif status == "MEDIUM":
        return "orange"
    else:
        return "red"

# -----------------------------
# 4. Read Serial Data
# -----------------------------
line = ser.readline().decode().strip()
# Example line from Arduino:
# 7.2,320,27,4,6.3,550,36,8

values = list(map(float, line.split(',')))
num_params = 4
num_samples = len(values)//num_params

samples = []
for i in range(num_samples):
    start = i*num_params
    sample_values = values[start:start+num_params]
    sample_dict = {param_names[j]: sample_values[j] for j in range(num_params)}
    samples.append(sample_dict)

# -----------------------------
# 5. Print Safe / Medium / Unsafe Status
# -----------------------------
for idx, sample in enumerate(samples):
    status = [classify(sample[param], param) for param in param_names]
    print(f"Sample {idx+1} Status:", status)

# -----------------------------
# 6. Plot Color-coded Graph
# -----------------------------
x = range(len(param_names))
plt.figure(figsize=(10,6))

for idx, sample in enumerate(samples):
    values = [sample[param] for param in param_names]
    colors = [get_color(classify(sample[param], param)) for param in param_names]
    
    # Plot each parameter point with its color
    for xi, val, color in zip(x, values, colors):
        plt.scatter(xi, val, color=color, s=100)
    plt.plot(x, values, label=f"Sample {idx+1}", linewidth=2)

plt.xticks(x, param_names)
plt.ylabel("Values")
plt.title("Water Quality Comparison (SAFE/MEDIUM/UNSAFE)")
plt.grid(True)
plt.legend()
plt.show()
