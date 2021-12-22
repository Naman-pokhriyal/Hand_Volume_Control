import cv2 as cv
import numpy as np
import time
import handModule as hm
import math
# 
import pyautogui as gui
# 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detect = hm.handDetector(maxHands =1, Confidence = 0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange =volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol =0
volBar =300
volPer =0
pTime =0
volCheck = False
count =0
while True:
    _, img = cap.read()
    img = cv.flip(img, 1)

    detect.findHands(img, True)
    lmList, bbox = detect.findPosition(img, draw=True)
    fingers = detect.fingerDown()

    
    

    if fingers == [12,16,20]:
        xmin, ymin, xmax, ymax = bbox[0],bbox[1],bbox[2],bbox[3]
        wH, hH = (xmax-xmin), (ymax-ymin)/100
        cv.circle(img, (lmList[0][1],lmList[0][2]), 3, (0,0,255), -1)

        mid_left = [xmin, int((ymin+ymax)/2)]
        cv.line(img, (xmax,ymin), (mid_left[0], mid_left[1]), (255,255,255), 2)
        markLn = math.hypot(mid_left[0]-xmax, mid_left[1]-ymin)
        length, img, center =detect.findDistance(4, 8, img) 
        cx = center[0]
        cy = center[1]
        if length<25:
            cv.circle(img, (cx,cy), 7,(0,0,255),-1)
        if length>markLn-35:
            cv.circle(img, (cx,cy), 7,(255,0,0),-1)

        volPer = np.interp(length, [25, markLn-35], [0,100])
        volPer = 10 * round(volPer/10)
        volBar = np.interp(volPer, [0, 100], [300,100])
        volume.SetMasterVolumeLevelScalar(volPer/100, None)

    cv.rectangle(img, (15, 100), (25, 300), (0,255,0), 2)
    cv.rectangle(img, (15, int(volBar)), (25, 300), (0,255,0), -1)
    cv.circle(img, (20, int(volBar)), 10, (250,230,230), -1 )
    cv.circle(img, (20, int(volBar)), 7, (255,144,30), -1 )
    cv.putText(img, f"{int(volPer)}%", (14,325), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,30), 2)

    # fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (0,12), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv.imshow("Web", img)
    if cv.waitKey(1) == ord("q"):
        break
