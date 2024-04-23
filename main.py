# main.py
from chirp_server import ChirpStackServer

# ANSI escape code for yellow text
YELLOW = "\033[93m"
RESET = "\033[0m"

if __name__ == "__main__":    
    try:
        while True:
            server = ChirpStackServer('', 8081)
            server.serve_forever()
    except KeyboardInterrupt:
        print(YELLOW + "Server stopped." + RESET)
