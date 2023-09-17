import threading
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse

# 리마인더 스레드를 저장할 리스트를 생성합니다.
reminder_threads = []


def create_app() -> Sanic:
    bot_app = Sanic("callback_server", configure_logging=False)

    @bot_app.post("/bot")
    def print_response(request: Request) -> HTTPResponse:
        """봇 응답을 콘솔에 출력하고 리마인더 스레드를 시작합니다."""
        bot_response = request.json.get("text")
        print(f"\n{bot_response}")

        # 만약 이미 리마인더 스레드가 실행 중이라면, 스레드를 취소하고 리스트에서 제거합니다.
        for thread in reminder_threads:
            if thread.is_alive():
                thread.cancel()
                reminder_threads.remove(thread)

        # 새로운 리마인더 스레드를 시작하고 리스트에 추가합니다.
        reminder_thread = threading.Timer(10, send_reminder)
        reminder_thread.start()
        reminder_threads.append(reminder_thread)

        body = {"status": "메시지 전송 완료"}
        return response.json(body, status=200)

    def send_reminder():
        """사용자의 응답이 없을 때 10초 후에 리마인더를 출력합니다."""
        print("답변을 기다리고 있어요~")

    return bot_app


if __name__ == "__main__":
    app = create_app()
    port = 5034

    print(f"{port}번 포트에서 콜백 서버를 시작합니다.")
    app.run("0.0.0.0", port)
