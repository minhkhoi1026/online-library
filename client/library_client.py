import socket
import json
import time
from utils import *

HOST = "127.0.0.1"  # The default server's hostname or IP address
PORT = 26100  # The default port used by the server

class library_client:
#-------------------PRIVATE AREA-------------------
    def __init__(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        self.__connected = True
        self.server = None
    
    def __update_connection_state(self):
        try:
            self.server.settimeout(3) # maximum time to wait for server
            msg = self.server.recv().decode('utf-8')
            self.server.settimeout(None)
            self.__connected = eval(msg)
        except:
            self.__connected = False

    def __del__(self):
        self.close_connect()
        
#-------------------PUBLIC AREA-------------------
    def connect(self, host = HOST):
        self.host = host
        self.port = PORT
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                server_addr = (self.host, self.port)
                self.server = socket.create_connection(server_addr, timeout = 5)
                self.server = socket_adapter(self.server) # wrap socket in personal interface
                self.__connected = True
                return ("Connected successfully at "+ host_to_str(*server_addr))
            except socket.error:
                print("Failed to connect to", host_to_str(*server_addr) + ". Retrying...")
                self.port += 1
                self.server = None
                if (self.port >= 26106):
                    return "Cannot connect to server!"
    
    def close_connect(self):
        try:
            self.server.send("QUIT".encode("utf-8"))
            self.server.close()
            self.__connected = False
            return True
        except:
            return False
    
    def is_alive(self):
        return self.__connected
    
    def log_in(self, username, password):
        # send request
        request = ' '.join(["LOGIN", username, password])
        self.server.send(request.encode("utf-8"))

        # check if server still connect
        self.__update_connection_state()
        if not self.__connected:
            return False

        #receive request
        msg = self.server.recv().decode("utf-8")
        return eval(msg)
    
    # sign 
    def sign_up(self, username, password):
        request = ' '.join(["SIGNUP", username, password])
        self.server.send(request.encode("utf-8"))

        # check if server still connect
        self.__update_connection_state()
        if not self.__connected:
            return False

        msg = self.server.recv().decode("utf-8")
        return eval(msg)
    
    # get list of book by cmd and detail of cmd
    # return list of books, each book contain (ID, name, type, author,)
    def get_list_book(self, cmd, detail):
        if (cmd not in ["F_ID", "F_NAME", "F_TYPE", "F_AUTHOR"]):
            return []
        request = ' '.join([cmd, detail])
        self.server.send(request.encode('utf-8'))

        # check if server still connect
        self.__update_connection_state()
        if not self.__connected:
            return []

        json_books = self.server.recv().decode('utf-8')
        books = json.loads(json_books)
        return books
    
    # get book content by id
    def get_book_content(self, id):
        request = ' '.join(["GETBOOK", id])
        self.server.send(request.encode('utf-8'))

        # check if server still connect
        self.__update_connection_state()
        if not self.__connected:
            return ('None', b'')

        ext = self.server.recv().decode('utf-8')
        content = self.server.recv()
        return (ext, content)

if __name__ == '__main__':
    client = library_client()
    client.connect()
    with open("test3.pdf", "wb") as f:
        ext, content = client.get_book_content('2')
        print(ext)
        if (ext == 'None'): exit()
        f.write(content)
    print(client.close_connect())