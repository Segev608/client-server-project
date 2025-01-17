from socket import *
import threading
from Server import handle_client
import ssl


# headers should be this size
HEADER_SIZE = 65
# the types are defining how do we going to treat the packet
HEADER_TYPES = {"DISCONNECT": "close-connection",
                "MESSAGE": "messaging",
                "ACTIVE_USERS": "active_sessions_now",
                "REGISTRATION": "register_username"}
# length and type for now
HEADER_TYPES_AMOUNT = 2
# client-destination/server-source port session
PORT = 9000
IP = gethostbyname(gethostname())
path = 'C:\\Users\\User\\'

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile=path+'public.cer', keyfile=path+'private.key')


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
            connection_stream = context.wrap_socket(connection, server_side=True)
            # the server sends the activated clients in order to remove them whenever client has disconnected
            new_client_thread = threading.Thread(target=handle_client.client_connection,
                                                 args=(connection_stream, address, self.ACTIVATED_CLIENTS))
            new_client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} connections")




