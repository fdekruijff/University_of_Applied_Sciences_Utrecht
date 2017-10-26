import json


class ClientNode:
    def __init__(self, ip_address, port, uuid, connection_handler):
        self.ip_address = ip_address
        self.port = port
        self.connection_handler = connection_handler
        self.uuid = uuid

        self.alarm_status = False
        self.alarm_tripped = False
        self.online = True
        self.is_gui = False

    def __str__(self):
        return (
            "{" +
            "\"ip_address\":\"" + str(self.ip_address) + "\"," +
            "\"port\":\"" + str(self.port) + "\"," +
            "\"uuid\":\"" + str(self.uuid) + "\"," +
            "\"alarm_status\":\"" + str(self.alarm_status) + "\"," +
            "\"alarm_tripped\":\"" + str(self.alarm_tripped) + "\"," +
            "\"online\":\"" + str(self.online) + "\"," +
            "\"is_gui\":\"" + str(self.is_gui) +
            "\"}")

