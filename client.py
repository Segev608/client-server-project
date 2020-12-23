import socket, ssl
from Server.server_activision import PORT, HEADER_SIZE, HEADER_TYPES, IP
from Utilities.Packets import *
from Utilities.MyColor import Colors
import sys
import os

username = sys.argv[1]

# initialize const values on client side
PORT = PORT
HEADER = HEADER_SIZE
DISCONNECT_FLAG = HEADER_TYPES["DISCONNECT"]
MESSAGE_FLAG = HEADER_TYPES["MESSAGE"]
SERVER_ADDRESS = IP

socket = socket.socket()
client_socket = ssl.wrap_socket(socket, ssl_version=ssl.PROTOCOL_TLSv1)
try:
    client_socket.connect((SERVER_ADDRESS, PORT))
except ConnectionRefusedError:
    print('The server is closed right now, try again later!')
    sys.exit()

# update the server about the client username
client_socket.send(Packet(registration=username).assemble_packet())

ACTIVE            = '~1~'
TO_ADMIN          = '~2~'
TO_CLIENT         = '~3~'
TERMINATE_SESSION = '~4~'
OP_BOARD          = '~5~'
EXIT              = '~6~'


def welcome_screen(name: str, **kwargs):
    if kwargs['initial']:
        print(f'\t\t\t\twelcome back ', end="")
        print(Colors.colorful_str(color="green", sentence=name))
    output = f'''
                        =========================== | ==========  
                        Operation                   | command    
                        =========================== | ==========  
                        Present active users        |   {ACTIVE} 
                        Send directly to admin      |   {TO_ADMIN}  
                        Send to specific user       |   {TO_CLIENT} [SOON!]
                        Stop current session        |   {TERMINATE_SESSION}   
                        Show operation board        |   {OP_BOARD}   
                        Exit                        |   {EXIT}   
                        =========================== | ==========\r  
    '''
    print(output)
    print("NOTE: symbol '~' located above Tab button on your keyboard")


def send_message_server(**kwargs):
    client_socket.send(Packet(message=kwargs['message']).assemble_packet())


def disconnect_session(**kwargs):
    client_socket.send(Packet(type='disconnect').assemble_packet())


def active_users(**kwargs):
    client_socket.send(Packet(type='active_users_on_server').assemble_packet())
    data = client_socket.recv(4096)
    import pickle
    active_list = pickle.loads(data)
    for user in active_list:
        if username != user:  # don't print the current user name
            print(f'{user.strip()} is connected right now')


def close_program(**kwargs):
    disconnect_session()
    client_socket.close()


HANDLE_USER_CHOICE = {
    ACTIVE: active_users,
    TO_ADMIN: send_message_server,
    TO_CLIENT: None,
    OP_BOARD: welcome_screen,
    EXIT: close_program
}

if __name__ == '__main__':
    try:
        import os
        os.system('cls')
        welcome_screen(username, initial=True)

        # TODO fix the option to show the board and to exit the program

        session = False
        user_input = None
        msg = ''
        # Control area for client
        while user_input != EXIT:
            # choose between different options
            if not session:
                user_input = input(f"[{username}]>> ")
                session = True if user_input in [TO_ADMIN] else False

            # start session with other client [in dev] or with admin
            if session:
                msg = input(f"[{username} - #message#]>> ")
                session = False if msg == TERMINATE_SESSION else True

            if user_input == TERMINATE_SESSION:
                print('\n[system]>> You are not in the middle of any session')
            else:
                HANDLE_USER_CHOICE[user_input](message=msg)
            # send_message_server(message)
    except ConnectionResetError:
        print('The server suddenly disconnected ')
    except KeyboardInterrupt:
        print('\n[system]>> Goodbye ')
    finally:
        # close connection and free the thread!
        close_program()
