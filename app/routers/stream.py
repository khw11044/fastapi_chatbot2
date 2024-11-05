from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.camera_service import open_camera, close_camera, get_camera_frame
import asyncio

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
        while True:
            # 프레임 가져오기
            frame = get_camera_frame(camera_id)
            if frame is None:
                await websocket.send_text("Failed to capture frame.")
                await websocket.close()
                break

            # 프레임을 Base64로 인코딩하여 전송
            await websocket.send_bytes(frame)
            await asyncio.sleep(0.05)  # 20 FPS 정도로 제한
    except WebSocketDisconnect:
        print(f"Client disconnected from Camera {camera_id} stream.")
    finally:
        # WebSocket 연결이 끊어지면 카메라 닫기
        close_camera(camera_id)
