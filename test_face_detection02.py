import cv2
import os 
import face_recognition

import time


cap=cv2.VideoCapture(0)                  # 0번 카메라에 연결

if cap.isOpened():                  
    while True:
        prevTime = time.time()
        
        ret, img = cap.read()              # 카메라를 읽습니다
        if ret:
            
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_img)
                
            name = "Unknown"
            # 결과를 출력합니다.
            for (top, right, bottom, left) in face_locations:
                print(top, right, bottom, left)
                left = int(left*0.9)
                right = int(right*1.1)
                top = int(top*0.8) 
                bottom = int(bottom*1.1) 
                
                # 얼굴에 상자와 이름을 표시합니다.
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (left + 10, bottom - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            
            curTime = time.time()
            sec = curTime - prevTime
            prevTime = curTime
            fps = 1/(sec)
            
            strfps = "FPS : %0.1f" % fps
            cv2.putText(img, strfps, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                    
            cv2.imshow('camera',img)     # 이미지를 표시합니다
            
            if cv2.waitKey(10) != -1:    # 10ms동안 키 입력을 대기
                break                    # 키가 입력되면 중지합니다

else:
    print("can't open camera")
cap.release()
cv2.destroyAllWindows()