import paho.mqtt.client as mqtt
import time

active_camera_sets = []
    

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

    global 
    if message.topic == "/ENEMIES/EP1":
        print("message from EP1")
        message_json = message.payload.decode("utf-8")
        active_camera_sets.push(message_json)

    if message.topic == "/ENEMIES/EP2":
        print("message from EP2")
        message_json = message.payload.decode("utf-8")
        active_camera_sets.push(message_json)

    if message.topic == "/ENEMIES/EP3":
        print("message from EP3")
        message_json = message.payload.decode("utf-8")
        active_camera_sets.push(message_json)

    if message.topic == "/ENEMIES/EP4":
        print("message from EP4")
        message_json = message.payload.decode("utf-8")
        active_camera_sets.push(message_json)

    print("number of enemies", NUM_ENEMIES_SEEN)
    if NUM_ENEMIES_SEEN == 0:
        pass

    elif NUM_ENEMIES_SEEN == 1:

        pass
    elif NUM_ENEMIES_SEEN == 2:
        pass

    elif NUM_ENEMIES_SEEN == 3:
        pass

def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribe topic", str(client), client, userdata, mid)

def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))

Connected = False

client = mqtt.Client("ENEMY_IC")
broker_address = "mosquitto.csse.rose-hulman.edu"
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

print("MQTT client connecting to host [" + broker_address + "]")
client.connect(broker_address, 1883, 60)
client.loop_start()

while Connected != True:
    time.sleep(0.1)

client.subscribe([("/ENEMIES/EP1", 0), ("/ENEMIES/EP2", 1), ("/ENEMIES/EP3", 2), ("/ENEMIES/EP4", 3)])

try:
    while True:
        # time.sleep(0.01)
        pass
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
