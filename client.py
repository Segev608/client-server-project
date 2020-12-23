import socket, ssl
from Server.server_activision import PORT, HEADER_SIZE, HEADER_TYPES, IP
from Utilities.Packets import *
from Utilities.MyColor import Colors, C_BALL
import sys
from subprocess import call
import os
import pickle

username = sys.argv[1]
colorful_username = Colors.colorful_str(color="red", sentence=username)

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


ACTIVE            = '~1'
TO_ADMIN          = '~2'
TO_CLIENT         = '~3'
TERMINATE_SESSION = '~4'
OP_BOARD          = '~5'
EXIT              = '~6'
COMMANDS = [f'~{i}' for i in range(1, 6)]


def welcome_screen(**kwargs):
    name = kwargs.get('u_name')
    if kwargs.get('initial'):
        print(f'\t\t\t\twelcome back ', end="")
        print(name)
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
    active_list = pickle.loads(data)
    connect = ''
    for user in active_list:
        user = user.strip()
        if not username == user:  # don't print the current user name
            connect += f'\t{Colors.colorful_str(color="green", sentence=C_BALL)} {user}\n'

    # no one connected to the server
    if len(connect) == 0:
        print('No one')
    # more then one client are active right now
    else:
        print(connect[:-1])


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

OUTPUT_TYPE = {
    'admin-message': Colors.colorful_str(color="yellow", sentence='#admin-message'),
    'session-message': Colors.colorful_str(color="yellow", sentence='#session-message'),
    'error': Colors.colorful_str(color="red", sentence='#error'),
    'logout': Colors.colorful_str(color="blue", sentence='#logout')
}

if __name__ == '__main__':
    try:
        # update the server about the client username
        client_socket.send(Packet(registration=username).assemble_packet())
        os.system('cls')
        welcome_screen(u_name=colorful_username, initial=True)

        session = False
        user_input = None
        msg = ''
        # Control area for client
        while user_input != EXIT:
            # choose between different options
            if not session:
                user_input = input(f"[{colorful_username}]>> ")

            # in case the user has inserted some input with any meanings, notify him
            if user_input not in COMMANDS:
                print(f'[system] - {OUTPUT_TYPE["error"]}>> Cannot understand your input')

            else:
                # start a session and begin message mode
                session = True if user_input in [TO_ADMIN] else False

                # close the chat program
                if user_input == EXIT:
                    print(f'\n[system] - {OUTPUT_TYPE["logout"]}>> Goodbye ')
                    break

                # start session with other client [in dev] or with admin
                if session:
                    if user_input == TO_ADMIN:
                        msg = input(f'[{colorful_username} - {OUTPUT_TYPE["admin-message"]}]>> ')
                    elif user_input == TO_CLIENT:
                        msg = input(f'[{colorful_username} - {OUTPUT_TYPE["session-message"]}]>> ')
                    session = False if msg == TERMINATE_SESSION else True

                # in case user wants to close the current session (admin/another client)
                if user_input == TERMINATE_SESSION:
                    print(f'\n[system] {OUTPUT_TYPE["error"]}>> You are not in the middle of any session')
                else:
                    HANDLE_USER_CHOICE[user_input](message=msg)
    except ConnectionResetError:
        print('The server suddenly disconnected ')
    except KeyboardInterrupt:
        # close the program with ctrl-c option
        print(f'\n[system] - {OUTPUT_TYPE["logout"]}>> Goodbye ')
    finally:
        # close connection and free the thread!
        close_program()
