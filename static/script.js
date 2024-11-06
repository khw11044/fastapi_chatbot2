let camera1WebSocket, camera2WebSocket;

// 카메라 ON/OFF 토글
function toggleCamera(cameraId) {
    const isOn = document.getElementById(`camera${cameraId}-toggle`).checked;
    const feedElement = document.getElementById(`camera${cameraId}-feed`);

    if (isOn) {
        // 카메라 켜기 - WebSocket을 통해 스트림 시작
        if (cameraId === 1) {
            camera1WebSocket = startStreamWebSocket(cameraId - 1, feedElement);
        } else if (cameraId === 2) {
            camera2WebSocket = startStreamWebSocket(cameraId, feedElement);
        }
    } else {
        // 카메라 끄기 - WebSocket 연결 종료 및 검은 화면 표시
        if (cameraId === 1 && camera1WebSocket) {
            camera1WebSocket.close();
            feedElement.src = ""; // 검은 화면 유지
        } else if (cameraId === 2 && camera2WebSocket) {
            camera2WebSocket.close();
            feedElement.src = ""; // 검은 화면 유지
        }
    }
}

// WebSocket을 통해 카메라 스트림 시작
function startStreamWebSocket(cameraId, feedElement) {
    const websocket = new WebSocket(`ws://localhost:8000/ws/stream?camera_id=${cameraId}`);

    websocket.onopen = () => {
        console.log(`Camera ${cameraId + 1} stream started.`);
    };

    websocket.onmessage = (event) => {
        const blob = event.data;
        const objectURL = URL.createObjectURL(blob);
        
        // requestAnimationFrame을 사용하여 화면에 최적화된 주기로 업데이트
        requestAnimationFrame(() => {
            feedElement.src = objectURL;
        });

        // 메모리 누수를 방지하기 위해 이전 Blob 객체를 해제
        feedElement.onload = () => {
            URL.revokeObjectURL(objectURL);
        };
    };

    websocket.onclose = () => {
        console.log(`Camera ${cameraId + 1} stream stopped.`);
    };

    return websocket;
}

// 음성 인식 ON/OFF 토글
let isVoiceRecognitionEnabled = false;

function toggleVoiceRecognition() {
    isVoiceRecognitionEnabled = document.getElementById("toggle-recognition").checked;
    if (isVoiceRecognitionEnabled) {
        startVoiceRecognition();
    }
}

// 음성 인식 시작 (비동기적으로 처리하여 카메라와 충돌 방지)
async function startVoiceRecognition() {
    while (isVoiceRecognitionEnabled) {
        try {
            const response = await fetch("/audio", { method: "POST" });
            const data = await response.json();

            if (data.transcription) {
                document.getElementById("user-input").value = data.transcription;
                sendMessage();
            }

            // 인식 후 1초 대기 (간격을 조정해 카메라와 충돌을 최소화)
            await new Promise(resolve => setTimeout(resolve, 1000));
        } catch (error) {
            console.error("Voice recognition error:", error);
            appendMessage("bot", "음성 인식 중 오류가 발생했습니다.");
            isVoiceRecognitionEnabled = false;
            document.getElementById("toggle-recognition").checked = false;
        }
    }
}

// 메시지를 전송하는 함수
async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message === "") return;

    appendMessage("user", message);
    userInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: message })
        });
        
        const data = await response.json();
        
        appendMessage("bot", data.answer);
    } catch (error) {
        console.error("Error:", error);
        appendMessage("bot", "에러가 발생했습니다. 다시 시도해주세요.");
    }
}

// 메시지를 chat-box에 추가하는 함수
function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.innerText = message;
    
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Enter 키를 눌러 메시지를 전송하는 이벤트 핸들러
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
