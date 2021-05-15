import socket

class server:
#-------------------PRIVATE AREA-------------------
    HOST = '127.0.0.1'  # The default server's hostname or IP address
    PORT = 26101  # The default port used by the server
    def __init__(self, host = HOST, port = PORT):
        self.host = host # server host IP
        self.port = port # server port
        # create new socket to listen
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
    
    def __del__(self):
        self.nr.close()
        self.nw.close()
        self.conn.close()
#-------------------PUBLIC AREA-------------------
    def listen_and_accept(self):
        self.s.listen()
        self.conn, self.addr = self.s.accept() # connection socket
        self.nr = self.conn.makefile(mode = 'r', encoding = 'utf-8') # stream reader
        self.nw = self.conn.makefile(mode = 'w', encoding = 'utf-8') # stream writer
        self.s.close()
        print('Connected by', self.addr)
    
    def close_connect(self):
        if (self.nr != None):
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.conn = None