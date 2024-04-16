# main.py
from chirp_server import ChirpStackServer


if __name__ == "__main__":    
    try:
        while True:
            server = ChirpStackServer('', 8081)
            server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")