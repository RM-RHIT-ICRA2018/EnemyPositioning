import cv2
import paho.mqtt.client as mqtt
import numpy as np
import math
import json
import time

ANGLE = 45
CAMERA_SET_ID = 0

def detect_object(frame, index, camera):
    st1 = time.time()
    if index == 'cam 2':
        frame = cv2.flip(frame,-1)
    frame_bgr = frame
    frame_rgb = np.asarray(cv2.cvtColor(
        frame_bgr, cv2.COLOR_BGR2RGB), dtype='uint8')
    #frame_rgb = frame_rgb[240:,:,:]
    fram_red = frame_rgb[:, :, 0]
    frame_gray = np.asarray(cv2.cvtColor(
        frame_rgb, cv2.COLOR_RGB2GRAY), dtype='uint8')
    frame_sub = np.maximum(np.subtract(
        fram_red, frame_gray, dtype='int8'), np.zeros([480,640]))
    frame_sub = frame_sub.astype('uint8')
    frame_filterd = cv2.medianBlur(frame_sub, 5)
   # cv2.imshow(index, frame_bgr)
   # return 1, 2
    ret, thresh = cv2.threshold(frame_sub, 25, 255, cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cx = 0
    cy = 0
    mikoto = 0
    if len(contours) != 0:
        for cont in contours:
            M = cv2.moments(cont)
            if M['m00'] > 50:
               #x, y, w, h, the = cv2.minAreaRect(cont)
               #cv2.drawContours(frame_bgr, cont, -1, 255, 3)
               #cv2.rectangle(frame_bgr, (x, y),
               #               (x + w, y + h), (0, 255, 0), 2)
               cx = int(M['m10']/M['m00'])
               cy = int(M['m01']/M['m00'])
               mikoto = 55/320*(cx-320)
               cv2.circle(thresh, (cx, cy), 3, (255, 255, 255), -1)
              # area = M['m00']
              # cv2.putText(frame_bgr, "Area: %f" % area, cv2.FONT_HERSHEY_SIMPLEX,
              #              0.5, (0, 255, 0), 2)
    #cv2.imshow(index,thresh)
    en1 = time.time()
    print("Pre TIme is %.2gs" %(en1-st1))
    return cx,cy, thresh, mikoto


def measure(cx1, cx2):
    dis = 0
    if cx1 != cx2:
        dis = 0.029*630*100/(cx2-cx1)
    if dis < 0:
        dis = -dis
    return dis


def process_camera(client,broker):
    hd = 480
    wd = 640
    camera1 = cv2.VideoCapture(0)
    camera2 = cv2.VideoCapture(1)

    # camera1.set(cv2.CAP_PROP_BRIGHTNESS, -10)
    camera1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    camera1.set(cv2.CAP_PROP_EXPOSURE, 0.0015)
    camera1.set(cv2.CAP_PROP_GAIN, 0.6)
    camera1.set(cv2.CAP_PROP_FRAME_WIDTH,wd)
    camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, hd)
    # camera1.set(cv2.CAP_PROP_CONTRAST, 32)
    camera2.set(cv2.CAP_PROP_GAIN, 0.6)
    camera2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    camera2.set(cv2.CAP_PROP_EXPOSURE, 0.0015)
   # camera2.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    camera2.set(cv2.CAP_PROP_FRAME_WIDTH,wd)
    camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, hd)
    # camera2.set(cv2.CAP_PROP_CONTRAST, 32)

    print("capture 1 is open: " + str(camera1.isOpened()))
    print("capture 2 is open: " + str(camera2.isOpened()))

    client.connect(broker, 1883, 60)
    client.loop_start()

    ret = 1
    ret2 = 1
    shana = 0
    if (ret & ret2):
        while True:
            start = time.time()
            ret, frame_bgr = camera1.read()
            ret2, frame_bgr_2 = camera2.read()
            en1 = time.time()
            print("Get TIme is %.2gs" %(en1-start))
            # detect target
            # cv2.imshow('ori', frame_bgr)
            cx1, cy1,th1, misaka1 = detect_object(frame_bgr, 'cam 1', camera1)
            cx2, cy2,th2, misaka2 = detect_object(frame_bgr_2, 'cam 2',camera2)
            shana = 0
           # if np.abs(cx1-cx2) > 20:
            shana = measure(cx1,cx2)
           # shana _xc = shana
            if cx1 == 0  | cx2 == 0:
                shana = 0
            misaka = (misaka1+misaka2)/2
            cv2.putText(th1,"distance:" + str(shana) + "cx1:" + str(cx1) +"cx2:" + str(cx2), (cx1-70,cy1+80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow('dis',th1)
           # cv2.putText(th1, "cx: " + str(cx) + " cy: " + str(cy), (cx + 20, cy + 20),
           #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            end = time.time()
            print("Total TIme is %.2gs" %(end-start))

            # measure distance
            # measure_distance(cx1, cy1, cx2, cy2)

            json_data = json.dumps({
                'TimeStamp': en1,
                'Distance': shana,
                'EnemyAngle': misaka,
                'EnemyXS': 0,
                'EnemyYS': 0,
                'EnemyPhi': 0
            })
            if shana != 0:
                print("Publishing message to topic", "ENEMIES/EnemyXC")
                client.publish("/ENEMIES/EnemyXC", json_data)
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
    start = time.time()
    client = mqtt.Client("EP1")
    broker_address = "192.168.1.2"
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback

    process_camera(client,broker_address)
    #process_camera()
    #end = time.time()
    #print("TIme is %.2gs" %(end-start))

if __name__ == "__main__":
    main()
