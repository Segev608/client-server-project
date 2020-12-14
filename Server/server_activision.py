from socket import *
import threading
from Server import handle_client


# headers should be this size
HEADER_SIZE = 65
# the types are defining how do we going to treat the packet
HEADER_TYPES = {"DISCONNECT": "close-connection", "MESSAGE": "messaging"}
# length and type for now
HEADER_TYPES_AMOUNT = 2
# client-destination/server-source port session
PORT = 9000
IP = gethostbyname(gethostname())


class Server:

    def __init__(self):
        # server basic configuration [port & header-size]
        self.PORT = PORT
        self.SERVER_IP = IP
        # initialize socket and binding
        self.SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
        self.SERVER_SOCKET.bind((self.SERVER_IP, self.PORT))
        self.ACTIVATED_CLIENTS = []

    def activate_service(self):
        self.SERVER_SOCKET.listen()
        while True:
            # client has connected to our socket
            connection, address = self.SERVER_SOCKET.accept()
            new_client_thread = threading.Thread(target=handle_client.client_connection, args=(connection, address))
            new_client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} connections")