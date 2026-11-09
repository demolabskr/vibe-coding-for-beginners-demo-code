"""파이썬 기본 기능만으로 만든 아주 작은 웹 서버.

실행: uv run python 04-reading-note/tiny_server.py [포트]
끄기: Ctrl+C
"""
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Hello(BaseHTTPRequestHandler):
    def do_GET(self):
        body = "<h1>안녕하세요</h1><p>요청한 주소: " + self.path + "</p>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


# 같은 포트에 서버를 두 번 띄우면 오류가 나게 한다(Windows는 이 설정이 켜져 있으면 두 번째 서버도 떠 버린다).
HTTPServer.allow_reuse_address = False

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
print(f"http://127.0.0.1:{port}/ 에서 기다립니다. 끄려면 Ctrl+C")
HTTPServer(("127.0.0.1", port), Hello).serve_forever()
