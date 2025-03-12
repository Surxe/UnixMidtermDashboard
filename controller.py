from view import *
import socket
import threading

#server_addresses = [('35.211.173.229', 3300), ('35.211.22.252', 3300), ('35.211.62.178', 3300)]  # Input server addresses in form of (IP, Port), and use the external IP address
server_addresses = [('127.0.0.1', 3300)]

class Controller:
    def __init__(self) -> None:
        # Declaring GUI root and other components
        self.root = tk.Tk()
        self.view = View(self.root, self)
        self.root.title("Computer Networks Project")
        self.root.geometry("800x600")
        # Declaring socket components
        self.sockets = []
        self.running = False

    def run(self) -> None:
        self.view.pack_widgets() # Display buttons, labels, etc.
        self.connect_to_servers() # Connect to servers
        self.root.mainloop() # Pull up the GUI

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

    def handle_server(self, sock, address) -> None:
        while True:
            try:
                # sock.send(b'echo "Hello from the client!"')
                # Wait to receive data from the server
                data = sock.recv(1024)
                # Print valid data, otherwise disconnect from the server and close the socket.
                if data:
                    print(f"Received from {address}: {data.decode('utf-8')}")
                else:
                    print(f"Disconnected from {address}")
                    self.sockets.remove(sock)
                    sock.close()
            # Print any error that occurred
            except Exception as e:
                print(f"Error receiving from {address}: {e}")
            if not self.sockets:
                # If no more sockets left in array, close the client.
                print("All connections closed. Stopping Client.")
                self.running = False
                break



if __name__ == "__main__":
    c = Controller()
    c.run()
