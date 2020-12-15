from Server import server_activision

FLAG_SEPERATOR = "|#|"
END_LINE = "\r\n"


# Client transfers readable data through the socket
class Message:
    def __init__(self, message: str):
        self.message = message

    def create_packet(self) -> bytes:
        msg_header = str(len(self.message)) + FLAG_SEPERATOR + server_activision.HEADER_TYPES["MESSAGE"]
        msg_header += END_LINE
        msg_header += self.message
        f_message = msg_header.encode()  # convert to utf-8
        f_message += b' ' * (server_activision.HEADER_SIZE - len(f_message))
        return f_message


# user wants to disconnect the socket & notify the server to free the thread
class Disconnect:
    @staticmethod
    def create_packet() -> bytes:
        msg_header = '16' + FLAG_SEPERATOR + server_activision.HEADER_TYPES["DISCONNECT"]
        msg_header += END_LINE
        f_message = msg_header.encode()  # convert to utf-8
        f_message += b' ' * (server_activision.HEADER_SIZE - len(f_message))
        return f_message
