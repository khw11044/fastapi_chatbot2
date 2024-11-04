import speech_recognition as sr
import sounddevice as sd

def my_stt() :
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:     # 마이크 열기 
        # print("주문을 부탁드립니다")
        # 백그라운드 노이즈를 줄이기 위해 환경 소음 인식
        recognizer.adjust_for_ambient_noise(source)
        # 마이크 입력 받기
        audio = recognizer.listen(source)
    
    try :
        mySpeech = recognizer.recognize_google(audio, language='ko-KR', show_all=False)
    
        return mySpeech
        
    except sr.UnknownValueError:
        print("Google 음성 인식이 오디오를 이해할 수 없습니다.")
    except sr.RequestError as e:
        print("Google 음성 인식 서비스에서 결과를 요청할 수 없습니다.; {0}".format(e))
