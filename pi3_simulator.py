import paho.mqtt.client as mqtt

pi_id = "EP3"


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


def main():
	global pi_id
    client = mqtt.Client(pi_id)
    broker_address = "192.168.1.2"
    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
	
	enemy_angle = 40
	angle_json = json.dumps({
		'EnemyAngle': enemy_angle
	})
	while True:
		client.publish("/ENEMIES/" + pi_id, angle_json)

if __name__ == "__main__":
    main()
