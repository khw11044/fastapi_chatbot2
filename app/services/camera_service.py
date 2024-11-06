import cv2
import time 
import mediapipe as mp
from utils.face_detection import get_face_bbox, get_face_bbox2, get_face_bbox3
# 카메라 스트림 관리를 위한 변수
camera_streams = {}
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def open_camera(camera_id):
    """특정 카메라 ID로 카메라를 열고 스트림을 시작합니다."""
    if camera_id in camera_streams:
        print(f"Camera {camera_id} is already open.")
        return camera_streams[camera_id]
    
    # 카메라 ID에 맞는 스트림 열기
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Cannot open camera {camera_id}")
        return None

    camera_streams[camera_id] = cap
    print(f"Camera {camera_id} opened.")
    return cap

def close_camera(camera_id):
    """특정 카메라 ID로 카메라를 닫고 스트림을 중지합니다."""
    cap = camera_streams.get(camera_id)
    if cap and cap.isOpened():
        cap.release()
        print(f"Camera {camera_id} closed.")
        del camera_streams[camera_id]
    else:
        print(f"Camera {camera_id} is not open.")

def get_camera_frame(camera_id, thereisface):
    """특정 카메라 ID의 현재 프레임을 캡처하여 반환합니다."""
    cap = camera_streams.get(camera_id)
    if not cap or not cap.isOpened():
        print(f"Camera {camera_id} is not open.")
        return None
    
    ret, frame = cap.read()
    prevTime = time.time()
    if not ret:
        print(f"Failed to capture frame from camera {camera_id}.")
        return None

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    
    if camera_id==0:
        frame, thereisface = get_face_bbox3(frame, mp_face_detection, thereisface)

        curTime = time.time()
        sec = curTime - prevTime
        fps = 1/(sec)
    else:
        curTime = time.time()
        sec = curTime - prevTime
        fps = 1/(sec * 100)
    
    strfps = "FPS : %0.1f" % fps
    cv2.putText(frame, strfps, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            
    return frame, thereisface

