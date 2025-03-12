from view import *
import socket
import select
import threading

#server_addresses = [('35.211.173.229', 3300), ('35.211.22.252', 3300), ('35.211.62.178', 3300)]  # Input server addresses in form of (IP, Port), and use the internal IP address
server_addresses = [('127.0.0.1', 3300)]

class Controller:
    def __init__(self) -> None:
        self.client = None
        self.root = tk.Tk()
        self.view = View(self.root, self)
        self.root.title("Computer Networks Project")
        self.root.geometry("800x600")
        self.receive_thread = None
        self.sockets = []
        self.running = False

    def run(self) -> None:
        self.view.pack_widgets()
        self.connect_to_servers()
        self.root.mainloop()

    def connect_to_servers(self) -> None:
        if not self.running:
            self.running = True
            self.sockets = []
            for address, port in server_addresses:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((address, port))
                    self.sockets.append(s)
                    print(f"Connected to {address}")
                except Exception as e:
                    print(f"Error connecting to {address}: {e}")
            if self.sockets:
                self.receive_thread = threading.Thread(target=self.handle_server)
                self.receive_thread.start()
        else:
            print("Client is already running")

    def handle_server(self) -> None:
        while self.running:
            read_sockets, _, _ = select.select(self.sockets, [], [])
            for sock in read_sockets:
                try:
                    # sock.send(b'echo "Hello from the client!"')
                    data = sock.recv(1024)
                    if data:
                        print(f"Received from {sock.getpeername()}: {data.decode('utf-8')}")
                    else:
                        print(f"Disconnected from {sock.getpeername()}")
                        self.sockets.remove(sock)
                        sock.close()
                except Exception as e:
                    print(f"Error receiving from {sock.getpeername()}: {e}")
                finally:
                    self.sockets.remove(sock)
                    sock.close()
            if not self.sockets:
                print("All connections closed. Stopping Client.")
                self.running = False
                break



if __name__ == "__main__":
    c = Controller()
    c.run()
