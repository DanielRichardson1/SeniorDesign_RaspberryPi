import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# Home: 10.0.0.52 
# Hotspot: 172.20.10.6


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("Topic: '" + msg.topic + "', Message: '" + str(msg.payload.decode()) + "'")
    if msg.topic == "state":
        if msg.payload.decode() == "calibrate":
            pass
        elif msg.payload.decode() == "evaluate":
            pass
    elif msg.topic == "sensor":
        pass

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('172.20.10.6', 1883)
client.subscribe("sensor", qos=1)
client.subscribe("state", qos=1)

client.loop_forever()
          
