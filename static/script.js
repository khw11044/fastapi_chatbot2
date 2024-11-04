let isVoiceRecognitionEnabled = document.getElementById("toggle-recognition").checked;

// 음성 On/Off 토글
function toggleVoiceRecognition() {
    isVoiceRecognitionEnabled = document.getElementById("toggle-recognition").checked;
    if (isVoiceRecognitionEnabled) {
        startVoiceRecognition();
    }
}

// 음성 인식 시작
async function startVoiceRecognition() {
    while (isVoiceRecognitionEnabled) {
        try {
            // 서버에 음성 인식 요청
            const response = await fetch("/audio", { method: "POST" });
            const data = await response.json();

            if (data.transcription) {
                document.getElementById("user-input").value = data.transcription;
                sendMessage(); // 자동으로 전송
            }
        } catch (error) {
            console.error("Voice recognition error:", error);
            appendMessage("bot", "음성 인식 중 오류가 발생했습니다.");
            isVoiceRecognitionEnabled = false; // 에러 발생 시 음성 인식 중지
            document.getElementById("toggle-recognition").checked = false;
        }
    }
}

// 메시지를 전송하는 함수
async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message === "") return; // 빈 메시지인 경우 전송하지 않음

    // 사용자의 메시지를 화면에 추가
    appendMessage("user", message);

    // 입력 필드 초기화
    userInput.value = "";

    try {
        // 서버에 메시지 전송
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: message })
        });
        
        const data = await response.json();
        
        // 서버에서 받은 챗봇의 응답을 화면에 추가
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
    chatBox.scrollTop = chatBox.scrollHeight; // 새로운 메시지에 따라 스크롤을 자동으로 내림
}

// Enter 키를 눌러 메시지를 전송하는 이벤트 핸들러
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
