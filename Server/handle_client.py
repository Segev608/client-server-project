from socket import *
from Server import server_activision


def client_connection(connection: socket, address: tuple):
    print("[NEW CONNECTION ESTABLISHED] "+str(address[0])+" connected")
    live_connection = True
    while live_connection:
        # collecting the header section [length|#|type]
        header = connection.recv(server_activision.HEADER_SIZE).decode()
        if len(header.split('|#|')) == server_activision.HEADER_TYPES_AMOUNT:
            m = header.split('|#|')
            length, flag = m[0], m[1].strip()  # last flag must be strip to get rid of spaces
            # client sent disconnect packet
            if flag == server_activision.HEADER_TYPES["DISCONNECT"]:
                print(f"[DISCONNECTING] {address} ")
                live_connection = False
            # client sent text message
            elif flag == server_activision.HEADER_TYPES["MESSAGE"]:
                # TODO change the current recv size to some MESSAGE_SIZE
                message = connection.recv(server_activision.HEADER_SIZE).decode()
                print(message)
            # reserved section
            else:
                print("HAVE NOT IMPLEMENTED YET")
    # client has disconnected from session
    connection.close()
