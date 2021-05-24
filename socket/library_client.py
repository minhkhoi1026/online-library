import socket
import json
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
                self.server = utils.socket_adapter(server) # wrap socket in different interface
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
            self.server.close()
            return True
        except:
            return False
    
    def log_in(self, username, password):
        request = ' '.join(["LOGIN", username, password])
        self.server.send(request.encode("utf-8"))
        msg = self.server.recv().decode("utf-8")
        return eval(msg)
    
    def sign_up(self, username, password):
        request = ' '.join(["SIGNUP", username, password])
        self.server.send(request.encode("utf-8"))
        msg = self.server.recv().decode("utf-8")
        return eval(msg)
    
    def get_list_book(self, cmd, detail):
        if (cmd not in ["F_ID", "F_NAME", "F_TYPE", "F_AUTHOR"]):
            return []
        request = ' '.join([cmd], detail)
        self.server.send(request.encode('utf-8'))
        json_books = self.server.recv().decode('utf-8')
        books = json.loads(json_books)
        return books
    
    def get_book_content(self, id):
        request = ' '.join(["GETBOOK"], id)
        self.server.send(request.encode('utf-8'))
        content = self.server.recv()
        return content

client = library_client()
client.connect()
client.close_connect()