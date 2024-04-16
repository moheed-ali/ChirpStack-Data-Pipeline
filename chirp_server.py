# chirp_server.py
from http.server import HTTPServer
from event_handlers import ChirpStackHandler

class ChirpStackServer:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.httpd = HTTPServer(self.server_address, ChirpStackHandler)

    def serve_forever(self):
        print(f"Server started on {self.server_address[0]}:{self.server_address[1]}")
        self.httpd.serve_forever()
