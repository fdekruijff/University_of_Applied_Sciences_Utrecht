import json


class ClientNode:
    def __init__(self, ip_address, port, uuid, connection_handler):
        self.ip_address = ip_address
        self.port = port
        self.connection_handler = connection_handler
        self.uuid = uuid

        self.alarm_tripped = False
        self.online = True

    def to_string(self) -> json:
        """ Returns JSON object of instance """
        return json.loads("{"
                          "'ip_address': {ip_address},"
                          "'port': {port},"
                          "'UUID': {uuid},"
                          "'alarm_tripped': {alarm_tripped},"
                          "'online': {online}}".format(
                            ip_address=self.ip_address,
                            port=self.port,
                            uuid=self.uuid,
                            alarm_tripped=self.alarm_tripped,
                            online=self.online
                            ))
