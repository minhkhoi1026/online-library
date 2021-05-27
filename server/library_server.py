import socket
import logging
import json
import threading
from database import library_database
from utils import *
import time

HOST = '0.0.0.0'  # open host in all network interfaces
PORT = 26100  # default port
DB_NAME = 'lb.db'
MAX_CONN = 5

class library_server:
#-------------------PRIVATE AREA-------------------
    def __init__(self, logger, host = HOST, port = PORT, db_name = DB_NAME, max_conn = MAX_CONN):
        self.host = host # server host IP
        self.port = port # server port
        self.db_name = db_name # server database name
        self.max_conn = max_conn
        self.client_threads = []
        self.logger = logger
    
#-------------------PUBLIC AREA-------------------
    def handle_client(self, client, addr):
        client = socket_adapter(client)
        database = library_database(self.db_name)

        def respond(request):
            tokens = request.split(' ')
            cmd = tokens[0]
            # Log in request, return True if the account exists
            # otherwise return False
            if cmd == "LOGIN":
                username = tokens[1]
                password = ' '.join(tokens[2:])
                if (database.log_in(username, password) == True):
                    client.send(b"True")
                else:
                    client.send(b"False")
            # Sign up request, create user and return True if the account have not exist
            # otherwise return False
            elif cmd == "SIGNUP":
                username = tokens[1]
                password = ' '.join(tokens[2:])
                if (database.sign_up(username, password) == True):
                    client.send(b"True")
                else:
                    client.send(b"False")
            # Find book request, return json string of list of books
            elif cmd.startswith("F_"):
                books = []
                if (cmd == "F_ID"):
                    id = tokens[1]
                    books = database.get_books_by_id(id)
                elif (cmd == "F_NAME"):
                    name = ' '.join(tokens[1:])
                    books = database.get_books_by_name(name)
                elif (cmd == "F_TYPE"):
                    book_type = ' '.join(tokens[1:])
                    books = database.get_books_by_type(book_type)
                elif (cmd == "F_AUTHOR"):
                    author = ' '.join(tokens[1:])
                    books = database.get_books_by_author(author)
                # dumps list of row into json strings then send to client
                json_books = json.dumps(books)
                client.send(json_books.encode('utf-8'))
            # Get content of book by id request, return binary string of file
            elif cmd == ("GETBOOK"):
                id = tokens[1]
                ext, content = database.get_book_content(id)
                client.send(ext.encode("utf-8"))
                client.send(content)
            else:
                return False
            return True
        
        while True:
            try:
                request = client.recv().decode("utf-8") # receive request

                # check if current thread is still able to running
                if threading.current_thread().is_stopped():
                    client.send(b"False")
                    break
                else:
                    client.send(b"True")

                # respond request
                if (request == "QUIT" or request == ""):
                    self.logger.log(logging.INFO, "Client " + host_to_str(*addr) + " closed successfully!")
                    break
                else:
                    if (respond(request) == True):
                        self.logger.log(logging.INFO, host_to_str(*addr) + ": Success to execute " + request)
                    else:
                        self.logger.log(logging.DEBUG, host_to_str(*addr) + ": Failed to execute " + request)
            # catch socket error
            except socket.error as msg: 
                self.logger.log(logging.ERROR, host_to_str(*addr) + " suddenly disconnected!")
                break
            # catch socket timeout
            except socket.timeout: 
                self.logger.log(logging.ERROR, host_to_str(*addr) + " connection time out!")   
                break
        # set state of thread and close connect
        threading.current_thread().stop()
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
                self.logger.log(logging.DEBUG, "Failed to deploy server at " + host_to_str(*server_addr) + ". Retrying...")
                self.port += 1
                if (self.port >= 26200):
                    raise RuntimeError("Cannot deploy server!")

        self.logger.log(logging.INFO, "Server is available at " + host_to_str(*server_addr))
        server.listen(0) # not allow queuing unaccpeted connection
        
        # accept connection then respond request from client
        while not threading.current_thread().is_stopped():
            try:
                client, addr = server.accept()
                if not (self.available()): # limited number of concurrent client
                    self.logger.log(logging.WARNING, host_to_str(*addr) + " refused due to limitation of server!")
                    client.close()
                    raise Exception
                # started new thread
                self.logger.log(logging.INFO, host_to_str(*addr) + " connected!")
                t = stoppabe_thread(target=self.handle_client, args=(client, addr))
                t.start()
                self.client_threads.append(t)
            except:
                pass
        server.close()
    
    # close all current connection
    def close_all_connect(self):
        for t in self.client_threads:
            if not t.is_stopped():
                t.stop()
        self.client_threads = []
        self.logger.log(logging.INFO, "Disconnected all client!")

    # update client list, remove thread that stopped
    def update_client_list(self):
        self.client_threads = [t for t in self.client_threads if not t.is_stopped()]

    # check if server capacity can accept new connection
    def available(self):
        self.update_client_list()
        return len(self.client_threads) < self.max_conn
        
