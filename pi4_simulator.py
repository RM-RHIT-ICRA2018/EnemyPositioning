import paho.mqtt.client as mqtt
import json

pi_id = "EP4"

def on_log(client, userdata, level, buf):
    print(level, buf)

def on_connect(client, userdata, flags, rc):
    print("connection callback")
    if rc == 0:
        print("Successfully connected with result code " + str(rc))
    else:
        print("Bad connection returned code=", rc)


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)



client = mqtt.Client(pi_id)
broker_address = "192.168.1.2"
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

print("MQTT client connecting to host [" + broker_address + "]")
client.connect(broker_address, 1883, 60)

client.loop_start()

enemy_angle = 40
angle_json = json.dumps({
   'EnemyAngle': enemy_angle
})

print("publishing topic")
client.publish("/ENEMIES/" + pi_id, angle_json)


