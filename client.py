import socket
from Server import server_activision
from Packets import *

# initialize const values on client side
PORT = server_activision.PORT
HEADER = server_activision.HEADER_SIZE
DISCONNECT_FLAG = server_activision.HEADER_TYPES["DISCONNECT"]
MESSAGE_FLAG = server_activision.HEADER_TYPES["MESSAGE"]
SERVER_ADDRESS = server_activision.IP

client_socket = socket.socket()
client_socket.connect((SERVER_ADDRESS, PORT))


def send_message(msg: str):
    client_socket.send(Message(msg).create_packet())


def disconnect_session():
    client_socket.send(Disconnect.create_packet())


send_message("message test 1")
input()
send_message("message test 2")
input()
send_message("message test 3")
input()

# close connection and free the thread!
disconnect_session()
