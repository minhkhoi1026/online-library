import socket
import logging
import json
from _thread import start_new_thread
from database import library_database
from utils import *

HOST = '0.0.0.0'  # open host in all network interfaces
PORT = 26100  # default port
MAX_CONN = 5

class library_server:
#-------------------PRIVATE AREA-------------------
    def __init__(self, host = HOST, port = PORT):
        self.host = host # server host IP
        self.port = port # server port
        self.database = library_database()
    
#-------------------PUBLIC AREA-------------------
    def communicate_client(self, client, addr):
        client = socket_adapter(client)

        def respond(request):
            tokens = request.split(' ')
            cmd = tokens[0]
            # Log in request, return True if the account exists
            # otherwise return False
            if cmd == "LOGIN":
                username = tokens[1]
                password = ' '.join(tokens[2:])
                if (self.database.check_log_in(username, password) == True):
                    client.send(b"True")
                else:
                    client.send(b"False")
            # Sign up request, create user and return True if the account have not exist
            # otherwise return False
            elif cmd == "SIGNUP":
                username = tokens[1]
                password = ' '.join(tokens[2:])
                if (self.database.sign_up(username, password) == True):
                    client.send(b"True")
                else:
                    client.send(b"False")
            # Find book request, return json string of list of books
            elif cmd.startswith("F_"):
                books = []
                if (cmd == "F_ID"):
                    id = tokens[1]
                    books = self.database.get_books_by_id(id)
                elif (cmd == "F_NAME"):
                    name = ' '.join(tokens[1:])
                    books = self.database.get_books_by_name(name)
                elif (cmd == "F_TYPE"):
                    book_type = ' '.join(tokens[1:])
                    books = self.database.get_books_by_type(book_type)
                elif (cmd == "F_AUTHOR"):
                    author = ' '.join(tokens[1:])
                    books = self.database.get_books_by_author(author)
                # dumps list of row into json strings then send to client
                json_books = json.dumps(books)
                client.send(json_books.encode('utf-8'))
            # Get content of book by id request, return binary string of file
            elif cmd == ("GETBOOK"):
                id = tokens[1]
                content = self.database.get_book_content(id)
                client.send(data)
            else:
                return False
            return True
                
        while True:
            try:
                client.settimeout(3)
                request = client.recv().decode("utf-8")
                if (request == "QUIT"):
                    print("Client " + host_to_str(addr) + " closed successfully!")
                    break
                else:
                    if (respond(request) == True):
                        print("Client " + host_to_str(addr) + ": Success to execute " + request)
                    else:
                        print("Client " + host_to_str(addr) + ": Failed to execute " + request)
            except socket.error as msg:
                print(msg + ". Client " + host_to_str(addr) + " suddenly disconnected!")
                break
            except socket.timeout:
                print((msg + ". Client " + host_to_str(addr) + " connection time out!")
            
            print(cmd)
            
        client.close()

    def run(self):
        # Open to listen for connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = None
        
        while True:
            try:
                server_addr = (self.host, self.port)
                server.bind(server_addr)
                break
            except socket.error:
                print("Failed to deploy server at", host_to_str(*server_addr) + ". Retrying...")
                self.port += 1
                if (self.port >= 26200):
                    raise RuntimeError("Cannot deploy server!")

        server.listen(MAX_CONN)
        server.setblocking(false)
        print("Server is available at",  host_to_str(*server_addr))

        # accept connection then respond request from client
        while True:
            client, addr = server.accept()
            print("Connected to:", host_to_str(*server_addr))
            '''try:
                start_new_thread(respond_client(client, addr))
            except :
                pass'''
            start_new_thread(self.communicate_client, (client, addr, ))
        server.close()
        
server = library_server()
server.run()
