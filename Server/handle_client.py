from socket import *
from Server import server_activision
from time import sleep
from Utilities import Packets
from logging import basicConfig, INFO, info
from datetime import date, datetime

path = "C:\\Users\\User\\PycharmProjects\\Workspace\\"


def session_log(client_session):
    # import logging
    # the name file will be stored as client_connection.log
    basicConfig(filename=path+'{}.log'.format(client_session.__name__), level=INFO)

    def wrapper(*args, **kwargs):
        today = date.today()
        now = datetime.now()
        info(f'client {args[1]} started a session in {today.strftime("%b-%d-%Y")} {now.strftime("%H:%M:%S")}')
        return client_session(*args, **kwargs)

    return wrapper


def get_username(users: list, conn: tuple):
    find = [user[2] if (user[0] == conn[0]) and (user[1] == conn[1]) else None for user in users]
    if find.__contains__(None):
        find.remove(None)
    if len(find) == 0:
        return None
    else:
        return find


@session_log
def client_connection(connection: socket, address: tuple, active_users: list):
    sleep(0.5)
    print("[NEW CONNECTION ESTABLISHED] "+str(address[0])+" connected")
    live_connection = True
    while live_connection:
        try:
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

            elif header.split(Packets.FLAG_SEPERATOR)[1] == server_activision.HEADER_TYPES["ACTIVE_USERS"]:
                # send the active connection to the client
                import pickle
                active = [name[2] for name in active_users]
                connection_list = pickle.dumps(active)
                connection.send(connection_list)

            # client sent data
            elif header.split(Packets.FLAG_SEPERATOR)[1] == server_activision.HEADER_TYPES["REGISTRATION"]:
                username = Payload  # user has registered with his nickname
                active_users.append((*address, username.strip()))  # store user info

            elif header.split(Packets.FLAG_SEPERATOR)[1] == server_activision.HEADER_TYPES["MESSAGE"]:
                today = date.today()
                now = datetime.now()
                info(f'client {get_username(active_users, address)} sent the message {Payload.strip()}'
                     f' {today.strftime("%b-%d-%Y")} {now.strftime("%H:%M:%S")}')

            # reserved section
            else:
                print("HAVE NOT IMPLEMENTED YET")
        except ConnectionResetError:
            print(f'{address} suddenly disconnected ')
            live_connection = False
            connection.close()
            active_users.remove(find_user(active_users, address))
            return
        except IndexError as e:
            print(str(e))
            return

    # client has disconnected from session
    active_users.remove(find_user(active_users, address))
    connection.close()


def find_user(users: list, addr: tuple):
    for user in users:
        ip, port, _ = user
        if addr == (ip, port):
            return user
