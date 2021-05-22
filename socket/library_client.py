import socket
import utils

HOST = "127.0.0.1"  # The default server's hostname or IP address
PORT = 26100  # The default port used by the server
BUF_SIZE = 256

class library_client:
#-------------------PRIVATE AREA-------------------
    def __init__(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        
#-------------------PUBLIC AREA-------------------
    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                server_addr = (self.host, self.port)
                self.server = socket.create_connection(server_addr, timeout = 0.5)
                print("Connected successfullt at", utils.host_to_str(*server_addr))
                break
            except socket.error:
                print("Failed to connect to", utils.host_to_str(*server_addr) + ". Retrying...")
                self.port += 1
                if (self.port >= 26200):
                    raise ConnectionError("Cannot connect to server!")
    
    def close_connect(self):
        try:
            self.server.send("QUIT".encode("utf-8"))
        except:
            pass

client = library_client()
client.connect()
client.close_connect()