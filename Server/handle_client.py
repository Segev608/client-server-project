from socket import *
from Server import server_activision
from time import sleep
from Utilities import Packets

path = "C:\\Users\\User\\PycharmProjects\\Workspace\\"


def session_log(client_session):
    # import logging
    from logging import basicConfig, INFO, info
    # the name file will be stored as client_connection.log
    basicConfig(filename=path+'{}.log'.format(client_session.__name__), level=INFO)

    def wrapper(*args):
        from datetime import date, datetime
        today = date.today()
        now = datetime.now()
        info(f'client {args[1]} started a session in {today.strftime("%b-%d-%Y")} {now.strftime("%H:%M:%S")}')
        return client_session(*args)

    return wrapper


@session_log
def client_connection(connection: socket, address: tuple, active_users: list):
    sleep(0.5)
    print("[NEW CONNECTION ESTABLISHED] "+str(address[0])+" connected")
    live_connection = True
    while live_connection:
        # collecting the header section [length|#|type\r\nMessage]
        packet = connection.recv(server_activision.HEADER_SIZE).decode()
        sections = packet.split(Packets.END_LINE)
        header = sections[0]
        Payload = None
        if len(sections) == 2:  # Payload exists
            Payload = sections[1]

        # client sent disconnect packet
        if header.split(Packets.FLAG_SEPERATOR)[1] == server_activision.HEADER_TYPES["DISCONNECT"]:
            print(f"[DISCONNECTING] {address} ")
            live_connection = False

        if header.split(Packets.FLAG_SEPERATOR)[1] == server_activision.HEADER_TYPES["ACTIVE_USERS"]:
            # send the active connection to the client
            import pickle
            connection_list = pickle.dumps(active_users)
            connection.send(connection_list)

        # client sent data
        if Payload:
            print(Payload)

        # reserved section
        else:
            print("HAVE NOT IMPLEMENTED YET")
    # client has disconnected from session
    active_users.remove(address)
    connection.close()
