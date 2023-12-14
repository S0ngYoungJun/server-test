from http.server import BaseHTTPRequestHandler, HTTPServer
import pymysql
import os

# 데이터베이스 연결 설정
db = pymysql.connect(host='localhost', user='root', password='723546', db='test', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# HTTP 요청 핸들러 클래스
class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        
        # 현재 스크립트가 위치한 디렉토리의 templates 폴더에 있는 index.html 파일 읽기
        with open(os.path.join(os.path.dirname(__file__), 'templates', 'index.html'), 'rb') as file:
            self.wfile.write(file.read())

# 서버 설정 및 실행
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()