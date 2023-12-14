from http.server import SimpleHTTPRequestHandler, HTTPServer
import pymysql
import os
import urllib.parse

# 데이터베이스 연결 설정
db = pymysql.connect(host='localhost', user='root', password='723546', db='test', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# HTTP 요청 핸들러 클래스
class RequestHandler(SimpleHTTPRequestHandler):
    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self._set_response()
            
            # 현재 스크립트가 위치한 디렉토리의 templates 폴더에 있는 index.html 파일 읽기
            with open(os.path.join(os.path.dirname(__file__), 'templates', 'index.html'), 'rb') as file:
                self.wfile.write(file.read())
        elif path == '/get_data':
            self._get_data()
        else:
            self._set_response(content_type='text/plain')
            self.wfile.write(b'Not Found')

    def _get_data(self):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM test")
            data = cursor.fetchall()

        self._set_response(content_type='application/json')
        self.wfile.write(str(data).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = urllib.parse.parse_qs(post_data)

        if self.path == '/create_data':
            self._create_data(data)

    def _create_data(self, data):
        data_value = data.get('data', [''])[0]

        with db.cursor() as cursor:
            cursor.execute("INSERT INTO test (data) VALUES (%s)", (data_value,))
            db.commit()

        self._set_response(content_type='application/json')
        self.wfile.write(b'{"status": "success"}')

# 서버 설정 및 실행
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
