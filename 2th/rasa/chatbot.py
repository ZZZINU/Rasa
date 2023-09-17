import requests


def send_message(message):  # 사용자의 메시지를 입력받아 Rasa 챗봇에 전달하고, 챗봇의 응답을 반환
    # Rasa 챗봇의 REST API 엔드포인트 주소를 변수 url에 저장합니다. 해당 주소로 POST 요청을 보내면 챗봇과 통신할 수 있습니다.
    # url = "http://localhost:5005/webhooks/rest/webhook"
    url = "http://localhost:5005/webhooks/callback/webhook"

    # 전송할 데이터를 리스트 형태로 생성합니다. 데이터는 JSON 형식으로 사용자의 sender와 message를 포함합니다.
    # data = [{"sender": "user", "message": message}]
    data = {"sender": "user", "message": message}

    # 요청 헤더를 설정합니다. 이 경우, JSON 형식의 데이터를 전송한다는 것을 명시합니다.
    headers = {"Content-type": "application/json"}

    # 함수를 사용하여 POST 요청을 보냅니다. url에 지정된 엔드포인트로 요청을 전송하고, 데이터와 헤더를 함께 전송합니다. 응답은 response 변수에 저장됩니다.
    response = requests.post(url, json=data, headers=headers)

    return response.json()  # 응답을 JSON 형식으로 반환합니다.


# 사용자 메시지를 입력하고 응답을 받는 함수
def chat():
    while True:
        user_input = input("나: ")  # 사용자에게 메시지를 입력받습니다.

        if user_input == "/stop":  # 사용자가 "/stop"을 입력하면 루프를 종료합니다.
            break

        # 사용자의 메시지를 send_message 함수를 사용하여 챗봇에 전달하고, 챗봇의 응답을 response 변수에 저장합니다.
        response = send_message(user_input)
        # print("Bot 응답:", response[0]['text'])
        for i in range (len(response)):
            print("Bot: ", response[i]['text'])


# chat 함수를 호출하여 대화 시작
chat()