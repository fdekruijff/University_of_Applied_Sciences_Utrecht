"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""


class Node:
    def __init__(self, ip_address: str, port: int, uuid: str, connection_handler):
        self.ip_address = ip_address
        self.port = port
        self.connection_handler = connection_handler
        self.uuid = uuid
        self.barrier_open = False
        self.online = False
        self.debug = False
        self.connected_to_server = False
        self.registered = False
        self.is_gui = False
        self.last_ping = 0.0

    def __str__(self):
        """ Returns object parameters in JSON string format for socket data transfer """
        return_string = "{"
        for x in range(len(self.__dict__.keys())):
            try:
                list(self.__dict__.keys())[x + 1] = list(self.__dict__.keys())[x + 1]
                return_string += (
                    "\"" +
                    str(list(self.__dict__.keys())[x]) + "\":\"" +
                    str(self.__dict__.get(list(self.__dict__.keys())[x])) +
                    "\","
                )
            except IndexError:
                return_string += (
                    "\"" +
                    str(list(self.__dict__.keys())[x]) + "\":\"" +
                    str(self.__dict__.get(list(self.__dict__.keys())[x]))
                )
        return return_string + "\"}"
