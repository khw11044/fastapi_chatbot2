# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routers import chatbot, audio, stream  

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 경로 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(chatbot.router)
app.include_router(audio.router)
app.include_router(stream.router)  # 라우터 등록

# 루트 경로에서 index.html 반환
@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)
