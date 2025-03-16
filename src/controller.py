import fileinput
import socket
import struct
import threading
import time
import os
import json
import subprocess

server_addresses = [('104.192.14.240', 12345), ('34.73.70.183', 12345), ('35.231.188.2', 12345)]  # Input server addresses in form of (IP, Port), and use the nic0 external IP address

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
                        print(f"Received from {server_address[0]}:{server_address[1]}: File Path: {response.decode('utf-8')}")
                        pathway = response.decode('utf-8').split("/")
                        sub_path = os.path.join(parent_dir, pathway[1], pathway[2])
                        print("Waiting for JSON length...")
                        json_length_data = client_socket.recv(4)
                        if len(json_length_data) < 4:
                            print("[!] Failed to receive JSON length")
                            exit()
                        json_length = struct.unpack('!I', json_length_data)[0]
                        print(f"[*] Expecting JSON of {json_length} bytes")
                        received_data = b""
                        while len(received_data) < json_length:
                            chunk = client_socket.recv(1024)
                            if not chunk:
                                break
                            received_data += chunk
                        json_str = received_data.decode('utf-8')
                        print(f"[*] Received JSON: {json_str[:100]}...")
                        json_data = json.loads(json_str)
                        with open(sub_path, "w") as file:
                            json.dump(json_data, file, indent=4)
                        subprocess.run(["python3", "validate_metrics.py"])
                        subprocess.run(["python3", "archive_metrics.py"])
                        time.sleep(60)
                    except (socket.error, ConnectionError):
                        print(f"Lost connection to {server_address[0]}:{server_address[1]}, reconnecting...")
                        break
            except (socket.error, ConnectionRefusedError) as e:
                print(f"Failed to connect to {server_address}, retrying...")
                time.sleep(5)


if __name__ == "__main__":
    c = Controller()
    c.start()