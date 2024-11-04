from fastapi import APIRouter, HTTPException
from app.services.audio_service import my_stt

router = APIRouter()

@router.post("/audio")
async def audio():
    try:
        transcription = my_stt()
        if transcription:
            return {"transcription": transcription}
        else:
            return {"transcription": ""}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))