import cv2
import paho.mqtt.client as mqtt
import numpy as np
import math
import json


def detect_object(frame_bgr):
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
    frame_hsv = cv2.GaussianBlur(frame_hsv, (3, 3), 1.2)

    # define range of color red in HSV space
    upper_red = np.array([10, 255, 255])
    lower_red = np.array([0, 100, 100])

    # create color red mask
    mask = cv2.inRange(frame_hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)

    M = cv2.moments(cnt)
    print(M)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cv2.imshow('orig', frame_bgr)
    cv2.imshow('frame', frame_hsv)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    return cx, cy


def process_camera(client, broker_address):
    camera1 = cv2.VideoCapture(0)
    camera2 = cv2.VideoCapture(1)
    camera3 = cv2.VideoCapture(2)
    camera4 = cv2.VideoCapture(3)
    # camera5 = cv2.VideoCapture(4)
    # camera6 = cv2.VideoCapture(5)
    # camera7 = cv2.VideoCapture(6)
    # camera8 = cv2.VideoCapture(7)
    camera1.set(cv2.CAP_PROP_BRIGHTNESS, 0.05)
    camera1.set(cv2.CAP_PROP_EXPOSURE, -9)
    print("capture device is open: " + str(camera1.isOpened()))
    print("capture device is open: " + str(camera2.isOpened()))
    print("capture device is open: " + str(camera3.isOpened()))
    print("capture device is open: " + str(camera4.isOpened()))
    client.connect(broker_address, 1883, 60)
    client.loop_start()
    ret = 1
    if (ret):
        while True:
            ret, frame_bgr = camera1.read()
            ret2, frame_bgr_2 = camera2.read()
            ret3, frame_bgr_3 = camera3.read()
            ret4, frame_bgr_4 = camera4.read()

            # detect target
            centroid_x, centroid_y = detect_object(frame_bgr)

            # measure distance
            measure_distance(marker)

            # calibrate both cameras
            # cv2.Calicv.CalibrateCamera2(, imageSize = 1920 * 1080)
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(25, 25))

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
