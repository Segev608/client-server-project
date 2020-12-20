import socket, ssl
from Server.server_activision import PORT, HEADER_SIZE, HEADER_TYPES, IP
from Utilities.Packets import *

# initialize const values on client side
PORT = PORT
HEADER = HEADER_SIZE
DISCONNECT_FLAG = HEADER_TYPES["DISCONNECT"]
MESSAGE_FLAG = HEADER_TYPES["MESSAGE"]
SERVER_ADDRESS = IP

socket = socket.socket()
client_socket = ssl.wrap_socket(socket, ssl_version=ssl.PROTOCOL_TLSv1)
client_socket.connect((SERVER_ADDRESS, PORT))


def send_message(msg: str):
    client_socket.send(Packet(message=msg).assemble_packet())


def disconnect_session():
    client_socket.send(Packet(disconnect=True).assemble_packet())


send_message("message test 1")
input()
send_message("message test 2")
input()
send_message("message test 3")
input()

# close connection and free the thread!
disconnect_session()
client_socket.close()
