import cv2
import paho.mqtt.client as mqtt
import numpy as np
import math
import json


def process_camera(client, broker_address):
    videoIn = cv2.VideoCapture(0)
    videoIn.set(cv2.CAP_PROP_BRIGHTNESS, 0.05)
    videoIn.set(cv2.CAP_PROP_EXPOSURE, -9)
    print("capture device is open: " + str(videoIn.isOpened()))
    client.connect(broker_address, 1883, 60)
    client.loop_start()
    ret = 1
    if (ret):
        while 1:
            ret, frame_bgr = videoIn.read()

            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
            frame_hsv = cv2.GaussianBlur(frame_hsv, (3, 3), 1.2)

            # define range of color red in HSV space
            upper_red = np.array([10, 255, 255])
            lower_red = np.array([0, 100, 100])

            # create color red mask
            mask = cv2.inRange(frame_hsv, lower_red, upper_red)

            res = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)

            cv2.imshow('orig', frame_bgr)
            cv2.imshow('frame', frame_hsv)
            cv2.imshow('mask', mask)
            cv2.imshow('res', res)

            # cv2.Calicv.CalibrateCamera2(, imageSize = 1920 * 1080)
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(25, 25))
            # frame = cv2.GaussianBlur(frame, (3, 3), 1.2);

            json_data = json.dumps({
                'EnemyXC': 0,
                'EnemyYC': 0,
                'EnemyAngle': 0,
                'EnemyXS': 0,
                'EnemyYS': 0,
                'EnemyPhi': 0
            })
            print("Publishing message to topic", "ENEMIES/EnemyXC")
            client.publish("ENEMIES/EnemyXC", json_data)
            cv2.waitKey(1)

    else:
        raise RuntimeError("Error while reading from camera.")
    client.loop_stop()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def main():
    client = mqtt.Client("EP1")
    broker_address = "127.0.0.1"
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback

    process_camera(client, broker_address)


if __name__ == "__main__":
    main()
