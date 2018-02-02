"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""


class Node:
    def __init__(self, ip_address: str, port: int, uuid: str, connection_handler, barrier_open=False, online=False,
                 debug=False, registered=False, is_gui=False, last_ping=0.0, water_level=0.0):
        self.ip_address = ip_address
        self.port = port
        self.connection_handler = connection_handler
        self.uuid = uuid
        self.barrier_open = barrier_open
        self.online = online
        self.debug = debug
        self.registered = registered
        self.is_gui = is_gui
        self.last_ping = last_ping
        self.water_level = water_level

    def __str__(self):
        """
            Dynamically transforms all this objects parameters and it's values to a JSON formatted style.
        """
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
