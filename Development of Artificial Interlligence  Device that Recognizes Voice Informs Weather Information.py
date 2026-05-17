import speech_recognition as sr  # 음성 인식 기능을 사용하기 위한 라이브러리
import requests  # OpenWeatherMap API 요청을 보내기 위한 라이브러리
import os  # 운영체제 명령어 실행을 위한 라이브러리
import time  # 시간 관련 기능 사용 라이브러리

API_KEY = "Enter your API key here"  # OpenWeatherMap API 키 입력
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"  # 서울 지역의 현재 날씨 정보를 요청하는 URL 생성


def speak(option, msg):  # 음성 출력 함수 정의
    os.system("espeak {} '{}'".format(option, msg))   # espeak 명령어를 이용하여 텍스트를 음성으로 출력
    
try:
    while True:  # 프로그램을 계속 반복 실행
        r = sr.Recognizer()  # 음성 인식 객체 생성

        with sr.Microphone() as source:  # 마이크를 입력 장치로 사용
            print("Say something!")  # 사용자에게 말하라는 메시지 출력
            audio = r.listen(source)  # 마이크로부터 음성을 입력받아 저장

        try:
            text = r.recognize_google(audio, language='ko-KR')  # Google 음성 인식 API를 이용하여 한국어 음성을 텍스트로 변환
            print("You said: " + text)  # 인식된 텍스트 출력
            if text in "날씨":  # 사용자가 "날씨" 관련 음성을 말했는지 확인
                print("날씨 음성을 인식하였습니다.")  # 인식 성공 메시지 출력
                response = requests.get(url)  # OpenWeatherMap API에 GET 요청 전송
                data = response.json()  # 응답 데이터를 JSON 형식으로 변환
                temp = data["main"]["temp"]  # 현재 기온 정보 추출
                humi = data["main"]["humidity"]  # 현재 습도 정보 추출
                msg = ' 기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'   # 음성 출력용 날씨 안내 문장 생성               
                option = '-s 180 -p 50 -a 200 -v ko+f5'  # espeak 음성 설정 -s : 말하는 속도, -p : 음높이, -a : 음량, -v : 음성 종류(한국어 여성 음성)
                speak(option, msg)  # 생성한 날씨 정보를 음성으로 출력

        except sr.UnknownValueError:      
            print("Google Speech Recognition could not understand audio") # 음성은 입력되었지만 내용을 인식하지 못한 경우

        except sr.RequestError as e:  
            print("Could not request results from Google Speech Recognition service; {0}".format(e)) # Google 음성 인식 서비스 요청 실패 시

except KeyboardInterrupt:  # Ctrl + C 입력 시 프로그램 종료
    pass

