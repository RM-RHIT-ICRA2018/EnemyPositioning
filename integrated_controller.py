import paho.mqtt.client as mqtt
import time
    

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected with result code " + str(rc))
        global Connected
        Connected = True
    else:
        print("Bad connection returned code=", rc)

def on_message(client, userdata, message):
    print("--------------")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if message.topic == "/ENEMIES/EP1":
        print("message from EP1")
        message_json = messages.payload.decode("utf-8")

    elif message.topic == "/ENEMIES/EP2":
        print("message from EP1")
        message_json = messages.payload.decode("utf-8")

    elif message.topic == "/ENEMIES/EP3":
        print("message from EP1")
        message_json = messages.payload.decode("utf-8")

    elif message.topic == "/ENEMIES/EP4":
        print("message from EP1")
        message_json = messages.payload.decode("utf-8")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribe topic", str(client), client, userdata, mid)

def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))

Connected = False

client = mqtt.Client("ENEMY_IC")
broker_address = "192.168.1.2"
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

print("MQTT client connecting to host [" + broker_address + "]")
client.connect(broker_address, 1883, 60)
client.loop_start()

while Connected != True:
    time.sleep(0.1)

client.subscribe([("/ENEMIES/EP1", 0), ("/ENEMIES/EP2", 1)])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
