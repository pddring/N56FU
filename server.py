from n56fu import N56FU
import socket
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

ports = N56FU.find_ports()

if ports:
    m = N56FU(ports[0])

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
       if self.path == '/value':
            response = json.dumps(m.get_reading())
            self.send_response(200)
       else:
            if self.path == '/':
                self.path = '/index.html'
        
            try:
                path = "static" + self.path
                with open(path) as f:
                    response = f.read()
                self.send_response(200)
            except:
                response = "File not found"
                self.send_response(404)
       self.end_headers()
       self.wfile.write(bytes(response, 'utf-8'))
ip = socket.gethostbyname(socket.gethostname())
port = 8080
print("Listening on: {}:{}".format(ip, port))

httpd = HTTPServer((ip, port),Serv)
httpd.serve_forever()