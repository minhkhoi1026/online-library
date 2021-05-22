import socket
import logging
from _thread import start_new_thread
import utils

HOST = '0.0.0.0'  # open host in all network interfaces
PORT = 26100  # default port
MAX_CONN = 5
BUF_SIZE = 256

class library_server:
#-------------------PRIVATE AREA-------------------
    def __init__(self, host = HOST, port = PORT):
        self.host = host # server host IP
        self.port = port # server port

#-------------------PUBLIC AREA-------------------
    def respond_client(self, client, addr):
        while True:
            cmd = client.recv(4).decode("utf-8")
            print(cmd)
            if (cmd == "QUIT"):
                print(utils.host_to_str(*addr) + " disconnected.")
                break
        client.close()

    def deploy(self):
        # Open to listen for connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = None
        
        while True:
            try:
                server_addr = (self.host, self.port)
                server.bind(server_addr)
                break
            except socket.error:
                print("Failed to deploy server at", utils.host_to_str(*server_addr) + ". Retrying...")
                self.port += 1
                if (self.port >= 26200):
                    raise RuntimeError("Cannot deploy server!")

        server.listen(MAX_CONN)
        print("Server is available at",  utils.host_to_str(*server_addr))

        # accept connection then respond request from client
        while True:
            client, addr = server.accept()
            print("Connected to:", utils.host_to_str(*server_addr))
            '''try:
                start_new_thread(respond_client(client, addr))
            except :
                pass'''
            start_new_thread(self.respond_client, (client, addr, ))
        server.close()
        
server = library_server()
server.deploy()
