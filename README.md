

cmake 설치 필요


pip install cmake

pip install dlib

pip install face-recognition


> uvicorn app.main:app --reload



```
project/
│
├── app/
│   ├── main.py                # FastAPI 앱 초기화
│   ├── routers/               # 라우터 모듈
│   │   ├── camera.py          # 카메라 관련 엔드포인트
│   │   ├── face_recognition.py # 얼굴 인식 엔드포인트
│   │   └── speech_recognition.py # 음성 인식 엔드포인트
│   ├── services/              # 서비스 모듈 (기능별 로직)
│   │   ├── camera_service.py   # 카메라 관련 로직
│   │   ├── face_service.py     # 얼굴 인식 로직
│   │   └── speech_service.py   # 음성 인식 로직
│   └── config/                # 설정 관련 모듈
│       └── settings.py         # CORS, DB 등 기타 설정
│
└── static/
    ├── index.html             # 메인 페이지
    ├── style.css              # CSS 파일
    └── script.js              # JavaScript 파일

```


# section01 

일단 웹으로 얼굴 인식 까지 


