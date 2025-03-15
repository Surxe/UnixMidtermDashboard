#from view import *
import socket
import threading
from threading import Thread

#server_addresses = [('35.211.173.229', 3300), ('35.211.22.252', 3300), ('35.211.62.178', 3300)]  # Input server addresses in form of (IP, Port), and use the external IP address
server_addresses = [('127.0.0.1', 3300)]

class Controller:
    def __init__(self) -> None:
        # Declaring socket components
        self.sockets = []
        self.running = False
        self.host = '127.0.0.1'
        self.port = 3300

    def run(self) -> None:
        self.connect_to_servers_test() # Connect to servers

    def connect_to_servers(self) -> None:
        if not self.running:
            # If the client is not running, set the running bool to true and clear sockets array
            self.running = True
            self.sockets = []
            for address, port in server_addresses:
                # For each IP and port in, attempt connections and add them to sockets array.
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((address, port))
                    self.sockets.append(sock)
                    print(f"Connected to {address}")
                    threading.Thread(target=self.handle_server, args=(sock, address), daemon=True).start()
                except Exception as e:
                    # Print out any error that occurred
                    print(f"Error connecting to {address}: {e}")
        else:
            print("Client is already running")

    def connect_to_servers_test(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(6)
            print(f"Listening on {self.host}:{self.port}")
            while True:
                conn, addr = sock.accept()
                self.sockets.append(conn)
                print(f"Received connection from IP {addr[0]} on port {addr[1]}")
                thread = Thread(target=self.handle_server, args=(conn, addr), daemon=True)
                thread.start()

    def handle_server(self, sock, address) -> None:
        while True:
            try:
                # Wait to receive data from the server
                data = sock.recv(1024)
                print(f"Received data from the server: {data.decode('utf-8')}")
                sock.send(b"Hello from the client!")
            # Print any error that occurred
            except Exception as e:
                print(f"Error receiving from {address}: {e}")
                sock.close()
                break



if __name__ == "__main__":
    c = Controller()
    c.run()