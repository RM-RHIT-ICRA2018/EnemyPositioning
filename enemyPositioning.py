import cv2
import paho.mqtt.client as mqtt
import numpy as np
import math
import json
import time


def detect_object(frame, index):
    frame_bgr = frame
    frame_rgb = np.asarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    frame_gray = np.asarray(cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY))
    
    # inds = np.where((frame_rgb[:, :, 1] < 250) & (frame_rgb[:, :, 1] < 250))
    # frame_rgb[inds] 
    frame_sub = frame_rgb[:, :, 0] - frame_gray

    frame_filterd = cv2.medianBlur(frame_sub, 3)

    # frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
    # frame_hsv = cv2.GaussianBlur(frame_hsv, (3, 3), 1.2)

    # define range of color red in HSV space
    # upper_red = np.array([10, 255, 255])
    # lower_red = np.array([0, 100, 100])

    # create color red mask
    # mask = cv2.inRange(frame_hsv, lower_red, upper_red)
    # res = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)

    ret, thresh = cv2.threshold(frame_filterd, 50, 1, cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh, 0, 1)
    max_count = -9999
    max_area = None
    for contour in contours:
        if len(contour) < 100:
            if len(contour) > max_count:
                max_count = len(contour)
                max_area = contour
        # print('------')
        # print(contour)
        # print(len(contour))
        # print('------')

    cx = 0
    cy = 0
    if len(contours) != 0:
        # max_area = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_area)
        cv2.drawContours(frame_bgr, max_area, -1, 255, 3)
        cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
        M = cv2.moments(max_area)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame_bgr, (cx, cy), 10, (0, 255, 0), -1)
            cv2.putText(frame_bgr, "cx: " + str(cx) + " cy: " + str(cy), (cx + 20, cy + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow(index, frame_bgr)
    return cx, cy


def measure_distance(cx1, cy1, cx2, cy2):
    
    pass


def process_camera(broker_address):
    camera1 = cv2.VideoCapture(1)
    camera2 = cv2.VideoCapture(2)
 
    camera1.set(cv2.CAP_PROP_BRIGHTNESS, -100)
    camera1.set(cv2.CAP_PROP_EXPOSURE, -13)
    # camera1.set(cv2.CAP_PROP_CONTRAST, 32)
    camera2.set(cv2.CAP_PROP_BRIGHTNESS, -100)
    camera2.set(cv2.CAP_PROP_EXPOSURE, -13)
    # camera2.set(cv2.CAP_PROP_CONTRAST, 32)

    print(camera1.get(cv2.CAP_PROP_BRIGHTNESS))
    print(camera1.get(cv2.CAP_PROP_EXPOSURE))
    
    print("capture 1 is open: " + str(camera1.isOpened()))
    print("capture 2 is open: " + str(camera2.isOpened()))

    # client.connect(broker_address, 1883, 60)
    # client.loop_start()

    ret = 1
    ret2 = 1
    if (ret & ret2):
        while True:
            #ret = camera1.grab()
            #ret = camera2.grab()
            ret, frame_bgr = camera1.read()
            ret2, frame_bgr_2 = camera2.read()

            # detect target
            cx1, cy1 = detect_object(frame_bgr, 'cam 1')
            cx2, cy2 = detect_object(frame_bgr_2, 'cam 2')

            # measure distance
            measure_distance(cx1, cy1, cx2, cy2)

            json_data = json.dumps({
                'EnemyXC': 0,
                'EnemyYC': 0,
                'EnemyAngle': 0,
                'EnemyXS': 0,
                'EnemyYS': 0,
                'EnemyPhi': 0
            })
            # print("Publishing message to topic", "ENEMIES/EnemyXC")
            # client.publish("ENEMIES/EnemyXC", json_data)
            cv2.waitKey(1)
    else:
        raise RuntimeError("Error while reading from camera.")
    # client.loop_stop()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def main():
    # client = mqtt.Client("EP1")
    broker_address = "127.0.0.1"
    # client.on_connect = on_connect  # attach function to callback
    # client.on_message = on_message  # attach function to callback

    process_camera(broker_address)


if __name__ == "__main__":
    main()
