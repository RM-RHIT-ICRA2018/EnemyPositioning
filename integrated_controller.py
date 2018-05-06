import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected with result code " + str(rc))
        client.subscribe("/ENEMIES")
    else:
        print("Bad connection returned code=", rc)

def on_message(client, userdata, message):
    print("here")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if message.topic == "/ENEMIES":
        print("message from enemies")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribe topic" + str(client))

def main():
    client = mqtt.Client("ENEMY_IC")
    broker_address = "192.168.1.2"
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    client.connect(broker_address, 1883, 60)
    print("MQTT client connecting to host [" + broker_address + "]")
    client.loop_forever()

if __name__ == "__main__":
    main()
