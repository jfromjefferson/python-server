import cgi
import json
from utils.requests import Requests
from http.server import BaseHTTPRequestHandler, HTTPServer


hostname = 'localhost'
server_port = 8000

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.requests: Requests = Requests()
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        length = int(self.headers.get('content-length'))
        data = json.loads(self.rfile.read(length))

        if data.get('item_id'):
            response = self.requests.get(id=data.get('item_id'))
        else:
            response = self.requests.get()

        return self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()

            message_dict = {
                'message': 'Not a valid JSON'
            }

            return self.wfile.write(json.dumps(message_dict).encode('utf-8'))

        length = int(self.headers.get('content-length'))
        data = json.loads(self.rfile.read(length))

        response = self.requests.post(data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        return self.wfile.write(json.dumps(response).encode('utf-8'))


    def do_PUT(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()

            message_dict = {
                'message': 'Not a valid JSON'
            }

            return self.wfile.write(json.dumps(message_dict).encode('utf-8'))
        
        length = int(self.headers.get('content-length'))
        data = json.loads(self.rfile.read(length))

        response = self.requests.put(**data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        return self.wfile.write(json.dumps(response).encode('utf-8'))

    
    def do_DELETE(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()

            message_dict = {
                'message': 'Not a valid JSON'
            }

            return self.wfile.write(json.dumps(message_dict).encode('utf-8'))
        
        length = int(self.headers.get('content-length'))
        data = json.loads(self.rfile.read(length))

        response = self.requests.delete(id=data.get('id'))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        return self.wfile.write(json.dumps(response).encode('utf-8'))
        

if __name__ == '__main__':
    web_server = HTTPServer((hostname, server_port), MyServer)
    print(f'Server started {hostname}:{server_port}')

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print('Server stopped.')