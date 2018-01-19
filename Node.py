"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""


class Node:
    def __init__(self, ip_address, port, uuid, connection_handler):
        self.ip_address = ip_address
        self.port = port
        self.connection_handler = connection_handler
        self.uuid = uuid

        self.barrier_open = False
        self.online = False
        self.is_gui = False

    def __str__(self):
        """ Returns object parameters in String format for socket data transfer """
        return (
            "{" +
            "\"ip_address\":\"" + str(self.ip_address) + "\"," +
            "\"port\":\"" + str(self.port) + "\"," +
            "\"uuid\":\"" + str(self.uuid) + "\"," +
            "\"online\":\"" + str(self.online) + "\"," +
            "\"barrier_open\":\"" + str(self.barrier_open) + "\"," +
            "\"is_gui\":\"" + str(self.is_gui) +
            "\"}")
