import socket
import threading
import time
import os
import json
from os.path import exists

#server_addresses = [('35.211.173.229', 3300), ('35.211.22.252', 3300), ('35.211.62.178', 3300)]  # Input server addresses in form of (IP, Port), and use the nic0 external IP address
server_addresses = [('34.73.13.5', 12345)]

parent_dir = "data"
sub_dirs = ["server1", "server2", "server3", "midterm-testing"]
nested_subdir = "archive"

class Controller:
    def __init__(self) -> None:
        # Declaring socket components
        self.sockets = {}
        self.running = True

    def start(self):
        os.makedirs(parent_dir, exist_ok=True)
        for sub in sub_dirs:
            os.makedirs(os.path.join(parent_dir, sub), exist_ok=True)
            os.makedirs(os.path.join(parent_dir, sub, nested_subdir), exist_ok=True)
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
                        client_socket.sendall(b"bash get_metrics.sh:python3 parse_metrics.py")
                        response = client_socket.recv(1024)
                        if not response:
                            raise ConnectionError
                        print(f"Received from {server_address[0]}:{server_address[1]}: {response.decode('utf-8')}")
                        pathway = response.decode('utf-8').split("/")
                        sub_path = os.path.join(parent_dir, pathway[1], pathway[2])
                        received_data = b""
                        while True:
                            chunk = client_socket.recv(1024)
                            if not chunk:
                                break
                            received_data += chunk
                        print(f"Received from {server_address[0]}:{server_address[1]}: All json data received")
                        json_data = json.loads(received_data.decode('utf-8'))
                        with open(os.path.join(sub_path, pathway[2]), "w") as file:
                            json.dump(json_data, file, indent=4)
                        time.sleep(5)
                    except (socket.error, ConnectionError):
                        print(f"Lost connection to {server_address[0]}:{server_address[1]}, reconnecting...")
                        break
            except (socket.error, ConnectionRefusedError) as e:
                print(f"Failed to connect to {server_address}, retrying...")
                time.sleep(5)


if __name__ == "__main__":
    c = Controller()
    c.start()