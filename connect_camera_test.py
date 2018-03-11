


import cv2

videoIn = cv2.VideoCapture(7)
videoIn.set(cv2.CAP_PROP_BRIGHTNESS,0.05)
print("capture device is open: " + str(videoIn.isOpened()))


# ### Step 3: Send webcam input to HDMI output

# In[307]:


import numpy as np

import math

ret = 1
if (ret): 
    while 1:
        ret, frame_webcam = videoIn.read()

        #frame_webcam = cv2.cvtColor(frame_webcam, cv2.COLOR_BGR2RGB);
        frame = cv2.cvtColor(frame_webcam, cv2.COLOR_RGB2HSV);

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(25, 25))  

        frame = cv2.GaussianBlur(frame, (3, 3), 1.2);
        mask1 = cv2.inRange(frame, np.array([100, 0, 125]), np.array([255, 255, 167]))

        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)  
        
        im2, contours, hierarchy = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
        cnt = {}
        times = 0
        try:
       
            for c in contours:
                # compute the center of the contour
                M = cv2.moments(c) 
                if M["m00"] and M["m10"] and M["m01"]:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cnt[times] = (cX, cY)
                    # draw the contour and center of the shape on the image
                    cv2.drawContours(frame_webcam, [c], -1, (0, 255, 0), 2)
                    cv2.circle(frame_webcam, (cX, cY), 7, (255, 255, 255), -1)
                    cv2.putText(frame_webcam, "Area:"+ str(int(M["m00"])), (cX+20, cY+20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    times = times+1
            cv2.line(frame_webcam, cnt[0], cnt[1],255,5)
            
            cv2.putText(frame_webcam, "pixcel dis:"+str(np.sqrt(np.square(cnt[0][0]-cnt[1][0])+np.square(cnt[0][1]-cnt[1][1])))+"pix", (100,450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            


            cv2.imshow("pic", frame)
            cv2.imshow("pic1", frame_webcam)
            cv2.waitKey(1)
        except:
            cv2.putText(frame_webcam, "invaild frame", (100,400),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow("pic", frame)
            cv2.imshow("pic1", frame_webcam)
            cv2.waitKey(1)
        
else:
    raise RuntimeError("Error while reading from camera.")
