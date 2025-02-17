import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import csv
import time

# Home: 10.0.0.52 
# Hotspot: 172.20.10.6

data = []  # List to store sensor data
collecting_data = False
start_time = 0

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global collecting_data, start_time, data
    print("Topic: '" + msg.topic + "', Message: '" + str(msg.payload.decode()) + "'")
    if msg.topic == "state":
        if msg.payload.decode() == "calibrate":
            collecting_data = True
            start_time = time.time()
            data = []  # Reset the data list
            print("Started data collection for calibration.")
        elif msg.payload.decode() == "evaluate":
            pass
    elif msg.topic == "sensor":
        if collecting_data:
            value = float(msg.payload.decode())
            timestamp = time.time() - start_time
            data.append((timestamp, value))
            print(f"Collected data: {timestamp}, {value}")
            if time.time() - start_time >= 60:
                collecting_data = False
                save_data_to_csv()
                print("Data collection completed and saved to CSV.")

def save_data_to_csv():
    global data
    with open('calibration_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Timestamp', 'Sensor Value'])
        csvwriter.writerows(data)
    print("Data saved to calibration_data.csv")

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('172.20.10.6', 1883)
client.subscribe("sensor", qos=1)
client.subscribe("state", qos=1)

client.loop_forever()
