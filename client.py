import socket, ssl
from Server.server_activision import PORT, HEADER_SIZE, HEADER_TYPES, IP
from Utilities.Packets import *
import sys

username = sys.argv[1]

# initialize const values on client side
PORT = PORT
HEADER = HEADER_SIZE
DISCONNECT_FLAG = HEADER_TYPES["DISCONNECT"]
MESSAGE_FLAG = HEADER_TYPES["MESSAGE"]
SERVER_ADDRESS = IP

socket = socket.socket()
client_socket = ssl.wrap_socket(socket, ssl_version=ssl.PROTOCOL_TLSv1)
client_socket.connect((SERVER_ADDRESS, PORT))

# update the server about the client username
client_socket.send(Packet(registration=username).assemble_packet())


def send_message(msg: str):
    client_socket.send(Packet(message=msg).assemble_packet())


def disconnect_session():
    client_socket.send(Packet(type='disconnect').assemble_packet())


def active_users():
    client_socket.send(Packet(type='active_users_on_server').assemble_packet())
    data = client_socket.recv(4096)
    import pickle
    active_list = pickle.loads(data)
    for user in active_list:
        if username != user:  # don't print the current user name
            print(f'{user.strip()} is connected right now')


if __name__ == '__main__':
    try:
        send_message("message test 1")
        input()
        send_message("message test 2")
        input()
        send_message("message test 3")
        input()
        active_users()
        input()
        # close connection and free the thread!
        disconnect_session()
    except ConnectionResetError:
        print('The server suddenly disconnected ')
    finally:
        client_socket.close()
