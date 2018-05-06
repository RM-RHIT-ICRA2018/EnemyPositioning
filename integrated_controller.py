import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected with result code " + str(rc))
    else:
        print("Bad connection returned code=", rc)

def on_message(client, userdata, message):
    print("--------------")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if message.topic.startswith("/ENEMIES")
        print("message from enemies")
        message_json = messages.payload.decode("utf-8")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribe topic", str(client), client, userdata, mid)


client = mqtt.Client("ENEMY_IC")startwith:
broker_address = "192.168.1.2"
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(broker_address, 1883, 60)
print("MQTT client connecting to host [" + broker_address + "]")
client.loop_start()
client.subscribe("/ENEMIES/EP4")

client.loop_forever()
