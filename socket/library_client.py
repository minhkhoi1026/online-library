import socket

class botnet_client:
#-------------------PRIVATE AREA-------------------
    HOST = '127.0.0.1'  # The default server's hostname or IP address
    PORT = 26101  # The default port used by the server
    def __init__(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #destructor of object
    def __del__(self):
        self.conn.close()
#-------------------PUBLIC AREA-------------------
    def connect(self):
        try:
            self.conn.connect((self.host, self.port)) # connection socket
            self.nr = self.conn.makefile(mode = 'r', encoding = 'utf-8') # stream reader
            self.nw = self.conn.makefile(mode = 'w', encoding = 'utf-8') # stream writer
            return "Connected successfully!"
        except:
            return "Connected failed"
        
    def close_connect(self):
        if (self.conn != None):
            self.send_message("QUIT")
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.conn = None