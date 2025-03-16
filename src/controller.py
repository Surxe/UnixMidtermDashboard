#from view import *
import socket
import threading
import time

#server_addresses = [('35.211.173.229', 3300), ('35.211.22.252', 3300), ('35.211.62.178', 3300)]  # Input server addresses in form of (IP, Port), and use the nic0 external IP address
server_addresses = [('127.0.0.1', 12345)]

class Controller:
    def __init__(self) -> None:
        # Declaring socket components
        self.sockets = {}
        self.running = True

    def start(self):
        for server in server_addresses:
            threading.Thread(target=self.handle_server, args=(server,)).start()

    def handle_server(self, server_address):
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5)
                client_socket.connect(server_address)
                print(f"Connected to {server_address[0]}:{server_address[1]}")
                while True:
                    try:
                        client_socket.sendall(b"bash src/stresser.sh:bash src/get_metrics.sh:python3 src/parse_metrics.py")
                        response = client_socket.recv(1024)
                        if not response:
                            raise ConnectionError
                        print(f"Received from {server_address[0]}:{server_address[1]}: {response.decode('utf-8')}")
                        time.sleep(300)
                    except (socket.error, ConnectionError):
                        print(f"Lost connection to {server_address[0]}:{server_address[1]}, reconnecting...")
                        break
            except (socket.error, ConnectionRefusedError) as e:
                print(f"Failed to connect to {server_address}, retrying...")
                time.sleep(5)


if __name__ == "__main__":
    c = Controller()
    c.start()