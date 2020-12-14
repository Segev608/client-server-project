import socket
from Server import server_activision

# initialize const values on client side
PORT = server_activision.PORT
HEADER = server_activision.HEADER_SIZE
DISCONNECT_FLAG = server_activision.HEADER_TYPES["DISCONNECT"]
MESSAGE_FLAG = server_activision.HEADER_TYPES["MESSAGE"]
SERVER_ADDRESS = server_activision.IP

client_socket = socket.socket()
client_socket.connect((SERVER_ADDRESS, PORT))

# TODO fix the send message, make different function for types
# prepare the message before sending
# the header defines the size of the next message
def send(message: str, flag):
    msg = message.encode()  # message in utf-8 to send
    msg_header = str(len(message)) + "|#|" + flag
    send_length = msg_header.encode()  # header in utf-8
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)  # notify the server about the length
    client_socket.send(msg)


send("message test 1", MESSAGE_FLAG)
input()
send("continue - test 2", MESSAGE_FLAG)
input()
send("continue - test 3", MESSAGE_FLAG)
input()

# close connection and free the thread!
send("bye bye", DISCONNECT_FLAG)
