# app/routers/chatbot.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import RagPipeline
from app.services.robot_service import process_order_response  # 함수 임포트


# 요청 데이터 구조 정의
class ChatRequest(BaseModel):
    question: str
    session_id: str = None

router = APIRouter()
rag_pipeline = RagPipeline()  # RAG 파이프라인 인스턴스 생성

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        print('[사용자]')
        print(request.question)
        answer = rag_pipeline.generate_answer(request.question, session_id=request.session_id)
        
        print('[AI]')
        print(answer)
        # 로봇 동작 수행
        process_order_response(answer["answer"])  # RAG 응답을 전달하여 로봇 동작 수행

        
        return {"answer": answer["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
