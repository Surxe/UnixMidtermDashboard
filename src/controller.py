import fileinput
import socket
import struct
import threading
import time
import os
import json
import subprocess

server_addresses = [('35.184.203.251', 12345), ('34.29.181.107', 12345), ('35.222.84.158', 12345)]  # Input server addresses in form of (IP, Port), and use the nic0 external IP address

parent_dir = "data"
sub_dirs = ["server1", "server2", "server3", "midterm-testing"]
nested_subdir = "archive"

class Controller:
    def __init__(self) -> None:
        # Declaring socket components
        self.sockets = {}
        self.running = True

    def start(self):
        os.makedirs(parent_dir, exist_ok=True) # make the parent directory if it doesnt already exist
        for sub in sub_dirs: # go through sub directories and make sub directories
            os.makedirs(os.path.join(parent_dir, sub), exist_ok=True)
            os.makedirs(os.path.join(parent_dir, sub, nested_subdir), exist_ok=True)
        for server in server_addresses: # start connection thread for each address
            threading.Thread(target=self.handle_server, args=(server,)).start()

    def handle_server(self, server_address):
        while True:
            try: #attempt to connect to servers
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5)
                client_socket.connect(server_address)
                print(f"Connected to {server_address[0]}:{server_address[1]}")
                while True:
                    try: # attempt to send commands to the server
                        client_socket.sendall(b"bash src/get_metrics.sh:python3 src/parse_metrics.py")
                        response = client_socket.recv(1024) # get file path response from server of where to put the json
                        print(f"Received from {server_address[0]}:{server_address[1]}: File Path: {response.decode('utf-8')}")
                        pathway = response.decode('utf-8').split("/")
                        sub_path = os.path.join(parent_dir, pathway[1], pathway[2])
                        print("Waiting for JSON length...") # receive the json file size
                        json_length_data = client_socket.recv(4)
                        if len(json_length_data) < 4:
                            print("[!] Failed to receive JSON length")
                            exit()
                        json_length = struct.unpack('!I', json_length_data)[0]
                        print(f"[*] Expecting JSON of {json_length} bytes")
                        received_data = b"" # receive the chunks of data from the json file contents
                        while len(received_data) < json_length:
                            chunk = client_socket.recv(1024)
                            if not chunk:
                                break
                            received_data += chunk
                        json_str = received_data.decode('utf-8') # decode the data and print part of file
                        print(f"[*] Received JSON: {json_str[:100]}...")
                        json_data = json.loads(json_str) # load the json string contents into the json file
                        with open(sub_path, "w") as file:
                            json.dump(json_data, file, indent=4)
                        subprocess.run(["python3", "validate_metrics.py"]) # run the scripts to validate and archive the metrics
                        subprocess.run(["python3", "archive_metrics.py"])
                        time.sleep(10)
                    except Exception as e: # error handling in case something happens
                        print(f"Lost connection to {server_address[0]}:{server_address[1]}, reconnecting...")
                        break
            except (socket.error, ConnectionRefusedError) as e: # error handling in case client could not connect to a server
                print(f"Failed to connect to {server_address}, retrying...")
                time.sleep(5)


if __name__ == "__main__":
    c = Controller()
    c.start()