from socket import *
from Server import server_activision
from time import sleep
from Utilities import Packets


def client_connection(connection: socket, address: tuple):
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

        # client sent data
        if Payload:
            print(Payload)

        # reserved section
        else:
            print("HAVE NOT IMPLEMENTED YET")
    # client has disconnected from session
    connection.close()
