import cv2 as cv
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands = 2, Confidence = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = Confidence
        self.trackCon = Confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handno=0, draw=True):
        xList=[]
        yList=[]
        bbox = 0
        self.lmList=[]
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = [xmin, ymin, xmax, ymax]
                self.lmList.append([id, cx, cy])
            if draw:
                # cv.putText(img, str(id), (cx, cy), cv.FONT_HERSHEY_PLAIN, 1, (255,0,255),2)
                cv.rectangle(img, (xmin-20,ymin-20), (xmax+20, ymax+20), (255, 0, 165), 1)

        return self.lmList, bbox
    
    def fingerDown(self):
        fingers=[]
        for finger in self.lmList:
            if finger[0]%4 ==0 and finger[0]>4:
                if finger[2] >= self.lmList[self.lmList.index(finger)-3][2]:
                    fingers.append(finger[0])

        return fingers 
    
    def findDistance(self, f1, f2, img, draw=True):
        x1, y1 = self.lmList[f1][1], self.lmList[f1][2] 
        x2, y2 = self.lmList[f2][1], self.lmList[f2][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        center = [cx, cy]
        length = math.hypot(x2 -x1, y2-y1)

        if draw:
            cv.circle(img, (x1,y1), 7,(0,255,0),-1) 
            cv.circle(img, (x2,y2), 7,(0,255,0),-1) 
            cv.line(img,(x1,y1), (x2,y2), (0,255,0), 2)
            cv.circle(img, (cx,cy), 7,(0,255,0),-1)
        
        return length, img, center




# def main():
#     cap = cv.VideoCapture(0)
#     # FPS
#     cTime=0
#     pTime=0
#     # CALLING
#     detect = handDetector(detectionCon=0.8)
#     fin=0
#     while True:
#         _, img = cap.read()
#         img = cv.flip(img, 1)
#         detect.findHands(img)
#         lmList = detect.findPosition(img, draw=False)
#         fingers =detect.fingerDown()
#         if len(fingers)!=0 and fin!=len(fingers):
#             print(len(fingers))
#             fin = len(fingers)
 

#         cTime = time.time()
#         fps = 1/(cTime - pTime)
#         pTime = cTime
#         cv.putText(img, str(int(fps)), (0, 15), cv.FONT_HERSHEY_PLAIN, 1, (255,0,255), 2)
        
#         cv.imshow("Cam", img)
#         if cv.waitKey(1) == ord('q'):
#             break




# if __name__ == "__main__":
#     main()