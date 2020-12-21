from Server import server_activision

FLAG_SEPERATOR = "|#|"
END_LINE = "\r\n"


# Client transfers readable data through the socket
class Packet:

    def __init__(self, **kwargs):
        self.message_type = None
        self.message = None
        if 'message' in kwargs.keys():
            self.message = kwargs['message']
            self.message_type = 'message'
        elif 'type' in kwargs.keys() and 'disconnect' in kwargs.values():
            self.message_type = 'disconnect'
        elif 'type' in kwargs.keys() and 'active_users_on_server' in kwargs.values():
            self.message_type = 'active_users_on_server'
        else:
            raise Exception('Unknown type of message')

    def assemble_packet(self):
        if self.message_type == 'message':
            return self.__create_packet_message()
        elif self.message_type == 'disconnect':
            return self.__create_packet_disconnect()
        elif self.message_type == 'active_users_on_server':
            return self.__create_packet_active_connections()

    def __create_packet_message(self) -> bytes:
        msg_header = str(len(self.message)) + FLAG_SEPERATOR + server_activision.HEADER_TYPES["MESSAGE"]
        msg_header += END_LINE
        msg_header += self.message
        f_message = msg_header.encode()  # convert to utf-8
        f_message += b' ' * (server_activision.HEADER_SIZE - len(f_message))
        return f_message

    def __create_packet_disconnect(self) -> bytes:
        msg_header = '16' + FLAG_SEPERATOR + server_activision.HEADER_TYPES["DISCONNECT"]
        msg_header += END_LINE
        f_message = msg_header.encode()  # convert to utf-8
        f_message += b' ' * (server_activision.HEADER_SIZE - len(f_message))
        return f_message

    def __create_packet_active_connections(self):
        msg_header = '24' + FLAG_SEPERATOR + server_activision.HEADER_TYPES["ACTIVE_USERS"]
        msg_header += END_LINE
        f_message = msg_header.encode()  # convert to utf-8
        f_message += b' ' * (server_activision.HEADER_SIZE - len(f_message))
        return f_message

