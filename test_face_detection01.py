
import cv2
import time 
import mediapipe as mp
from utils.face_detection import get_face_bbox

cap = cv2.VideoCapture(0)

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

while cap.isOpened():
    prevTime = time.time()
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    frame = get_face_bbox(frame, mp_face_detection)
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1/(sec)
    
    
    strfps = "FPS : %0.1f" % fps
    cv2.putText(frame, strfps, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
   
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    ###################################
    cv2.imshow('video',frame)
    if cv2.waitKey(10) != -1:    # 10ms동안 키 입력을 대기
        break                    # 키가 입력되면 중지합니다

cap.release()
cv2.destroyAllWindows()