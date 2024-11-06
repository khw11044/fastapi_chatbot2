from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.camera_service import open_camera, close_camera, get_camera_frame
import asyncio
import time 
import cv2
import httpx

router = APIRouter()

@router.websocket("/ws/stream")
async def camera_stream(websocket: WebSocket, camera_id: int):
    """WebSocket을 통해 특정 카메라 스트림을 제공합니다."""
    await websocket.accept()
    print(f"Client connected for Camera {camera_id} stream.")

    # 카메라 열기
    cap = open_camera(camera_id)
    if cap is None:
        await websocket.send_text("Failed to open camera.")
        await websocket.close()
        return

    try:
        thereisface = []
        face_cnt = 0
        session_id = None
        session_id_cnt = 0
        while True:

            # 프레임 가져오기
            frame, thereisface, face_cnt = get_camera_frame(camera_id, thereisface, face_cnt)
            if frame is None:
                await websocket.send_text("Failed to capture frame.")
                await websocket.close()
                break
            
            if face_cnt >= 15 and len(thereisface) > 0 and not session_id:
                session_id = thereisface[0]
            else:
                session_id = None
            
            if session_id and session_id_cnt==0:
                await send_session_to_chatbot(session_id)
                session_id_cnt = 1
            
            if face_cnt < 15 and session_id_cnt==1:
                session_id_cnt = 0
            
            # 프레임을 JPEG로 인코딩
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            jpeg_frame = jpeg_frame.tobytes()
            await websocket.send_bytes(jpeg_frame)
            await asyncio.sleep(0.05)  # 20 FPS 정도로 제한
    except WebSocketDisconnect:
        print(f"Client disconnected from Camera {camera_id} stream.")
    finally:
        # WebSocket 연결이 끊어지면 카메라 닫기
        close_camera(camera_id)

async def send_session_to_chatbot(session_id: str):
    """chatbot API에 session_id를 전송하는 함수"""
    url = "http://localhost:8000/chat"  # chatbot API의 엔드포인트 URL
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={"question": "init", "session_id": session_id})
            if response.status_code == 200:
                print(f"Session ID {session_id} successfully sent to chatbot.")
            else:
                print(f"Failed to send Session ID {session_id} to chatbot. Status code: {response.status_code}")
        except httpx.RequestError as e:
            print(f"An error occurred while sending session ID: {e}")