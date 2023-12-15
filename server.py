from http.server import SimpleHTTPRequestHandler, HTTPServer
import pymysql
import os
import urllib.parse
import json

# 데이터베이스 연결 설정
db = pymysql.connect(host='localhost', user='root', password='723546', db='test', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# HTTP 요청 핸들러 클래스
class RequestHandler(SimpleHTTPRequestHandler):
    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _serve_file(self, filename):
        file_path = os.path.join(os.path.dirname(__file__), 'templates', filename)

        try:
            with open(file_path, 'rb') as file:
                content = file.read()

            _, extension = os.path.splitext(filename)
            content_type = {
                '.html': 'text/html',
                '.js': 'application/javascript',
                '.json': 'application/json',
                # 다른 확장자에 대한 설정 추가
            }.get(extension, 'text/plain')

            self._set_response(content_type=content_type)
            self.wfile.write(content)
        except FileNotFoundError:
            self._set_response(content_type='text/plain')
            self.wfile.write(b'File Not Found')
        except Exception as e:
            print(f"Error in _serve_file: {str(e)}")
            self._set_response(content_type='text/plain')
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))

    def _get_data(self):
        try:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM data")
                data = cursor.fetchall()

            self._set_response(content_type='application/json')
            self.wfile.write(json.dumps(data).encode('utf-8'))
        except Exception as e:
            print(f"Error in _get_data: {str(e)}")
            self._set_response(content_type='text/plain')
            self.wfile.write(f'Error in _get_data: {str(e)}'.encode('utf-8'))

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self._serve_file('index.html')
        elif path == '/app.js':
            self._serve_file('app.js')
        elif path == '/get_data':
            self._get_data()
        else:
            self._set_response(content_type='text/plain')
            self.wfile.write(b'Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if self.path == '/create_data':
            self._create_data(data)

    def _create_data(self, data):
        try:
            data_value = data.get('data', ['']).strip()

            print(f"Received data: {data_value}")

            if data_value:  # 빈 문자열이 아닌 경우에만 데이터베이스에 추가
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO data (data) VALUES (%s)", (data_value,))
                    db.commit()

            self._set_response(content_type='application/json')
            self.wfile.write(b'{"status": "success"}')
        except Exception as e:
            print(f"Error in _create_data: {str(e)}")
            self._set_response(content_type='text/plain')
            self.wfile.write(f'Error in _create_data: {str(e)}'.encode('utf-8'))

# 서버 설정 및 실행
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
