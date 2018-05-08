import paho.mqtt.client as mqtt
import json
import time

pi_id = "EP2"

def on_log(client, userdata, level, buf):
    print(level, buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected with result code " + str(rc))
        global pi_id
        client.publish("/ENEMIES/" + pi_id)
    else:
        print("Bad connection returned code=", rc)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))
    client.loop_stop()

client = mqtt.Client(pi_id)
broker_address = "192.168.1.2"
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.on_disconnect = on_disconnect

print("MQTT client connecting to host [" + broker_address + "]")
client.connect(broker_address, 1883, 60)

# client.loop_start()

enemy_angle = 40
angle_json = json.dumps({
   'EnemyAngle': enemy_angle
})

print("publishing topic")
while True:
    time.sleep(0.01)
    client.publish("/ENEMIES/" + pi_id, angle_json)
    client.loop(0.03)
