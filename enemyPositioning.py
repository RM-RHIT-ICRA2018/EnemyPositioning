import cv2
import paho.mqtt.client as mqtt
import numpy as np
import math

videoIn = cv2.VideoCapture(1)
videoIn.set(cv2.CAP_PROP_BRIGHTNESS,0.05)
videoIn.set(cv2.CAP_PROP_EXPOSURE, 10)
print("capture device is open: " + str(videoIn.isOpened()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def process_camera():
	ret = 1
	if (ret): 
		while 1:
			ret, frame_webcam = videoIn.read()

			#frame_webcam = cv2.cvtColor(frame_webcam, cv2.COLOR_BGR2RGB);
			frame = cv2.cvtColor(frame_webcam, cv2.COLOR_RGB2HSV)

			# define range of color red in HSV space
			upper_red = np.array([10, 255, 255])
			lower_red = np.array([0, 100, 100])

			# create color red mask
			mask = cv2.inRange(frame, lower_red, upper_red)

			res = cv2.bitwise_and(frame, frame, mask= mask)

			cv2.imshow('orig', frame_webcam)
			cv2.imshow('frame', frame)
			cv2.imshow('mask', mask)
			cv2.imshow('res', res)
			# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(25, 25))  
			# frame = cv2.GaussianBlur(frame, (3, 3), 1.2);
			cv2.waitKey(1)
	else:
		raise RuntimeError("Error while reading from camera.")



# def on_connect(client, userdata, flags, rc):
#     print(BSP_ERROR.notice("MQTT Interface Bind Success."))
#     client.subscribe("/CANBUS/#")
#     print(BSP_ERROR.notice("MQTT Subscribe Success, Topic: /CANBUS/#, Start Receiving CAN Messages."))
#     t = threading.Thread(target = CAN_RCV_LOOP)
#     t.start()

# def on_message(client, userdata, msg):
#     print(BSP_ERROR.info("Topic: "+ msg.topic + " Payload: " + msg.payload))
#     payload = json.loads(msg.payload)
#     if payload.Type == "MotorTye":
#         can_pkt = struct.pack(fmt, int(payload.ID),8,bytes(payload.Torques))
#         sock.send(can_pkt)
#         print(BSP_ERROR.info("SocketCAN Package Send"))

def main(parameter_list):
    process_camera()
