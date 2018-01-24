"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""

import datetime
import socket
import sys
import json
import time
from _thread import *

from Node import Node


class Server:
    def __init__(self, host, port, debug):
        self.host = host
        self.port = port
        self.client_list = []
        self.debug = debug
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.barrier_open = False
        self.operational = True

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    def change_barrier(self):
        """ Open or close barrier based on variable """
        pass

    def init_socket(self) -> None:
        """ Initialises server socket """
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)
        except socket.error as e:
            if self.debug: print("{} - Socket error {}".format(Server.get_time(), e))
            sys.exit()
        finally:
            if self.debug: print("{} - Successfully bound to socket, PORT:{}".format(Server.get_time(), self.port))

    def find_client(self, client_uuid: str) -> Node:
        """ Returns the ClientNode object that matches the passed UUID """
        for x in self.client_list:
            if client_uuid == x.uuid:
                return x

    def remove_client(self, client_uuid: str) -> None:
        """
            Removes a client from the client list, this includes closing the connection handler and updating the status
        """
        client = self.find_client(client_uuid)
        if client:
            client.online = False
            client.connection_handler.close()
            self.client_list.remove(client)
            if self.debug:
                print("{} - Client with UUID {} has lost connection and has been unregistered.".format(
                    Server.get_time(), client_uuid))

    def send_client_data(self) -> str:
        """ Formats ClientObject parameter JSON data for all clients in client_list """
        return_string = "{"
        for client in self.client_list:
            return_string = return_string + str(client) + ','
        return_string = return_string[:-1]
        return_string += "}"
        return return_string

    def parse_socket_data(self, client_uuid: str, data_header: str, data: str) -> str or None:
        """ Handles socket data accordingly, can be either data or a data_header as data type """
        client = self.find_client(client_uuid)
        if data_header == "IS_ALIVE" and data == "ACK":
            client.last_ping = time.time()
        elif data_header == "BARRIER_STATUS":
            client.barrier_open = json.loads(data)['barrier_open']
            self.change_barrier()
        elif data_header == "UUID":
            return str(data)
        elif data_header == "GUI_UPDATE_REQ":
            self.socket_write(client.connection_handler, "CLIENT_DATA,{}".format(self.send_client_data()), client.uuid)
            # client.connection_handler.send(str(str(client.uuid) + ",CLIENT_DATA," + self.send_client_data()).encode('ascii'))

    def socket_write(self, conn, message: str, client_uuid: str) -> None:
        """
            Generic function that writes a concatenation of the client UUID
            and the message data to the passed connection socket
        """
        if not client_uuid:
            # Broadcast
            message = "BROADCAST" + "," + message
        else:
            # Unicast
            message = str(client_uuid) + "," + message

        if self.debug: print("{} - Server send: {}".format(Server.get_time(), message))
        try:
            conn.send(message.encode('ascii'))
        except:
            self.remove_client(client_uuid)

    def socket_read(self, connection):
        """
            Generic function that listens to the connection parameter socket and passes that data
            to the parse_socket_data() function
        """
        while True:
            try:
                data = connection.recv(4096).decode('utf-8').strip().split(',')
                if self.debug: print("{} - Server received: {}".format(Server.get_time(), data))
                try:
                    if data[0] or data[1] or data[2]:
                        pass
                except IndexError:
                    continue
                self.parse_socket_data(data[0], data[1], data[2])
            except Exception:
                if self.debug: print("{} - Cannot connect to client".format(Server.get_time()))
                for client in self.client_list:
                    try:
                        self.socket_write(client.connection_handler, "", "")
                    except Exception:
                        if self.debug: print(
                            "{} - Client with UUID {} has lost connection and has been unregistered.".format(
                                Server.get_time(), client.uuid))
                        self.remove_client(client.uuid)
                return

    def get_uuid(self, connection) -> str:
        """ Function is used during client registration to request client for their UUID """
        self.socket_write(connection, "UUID_REQ", "")
        try:
            data = connection.recv(2048).decode('utf-8').strip().split(',')
            return str(self.parse_socket_data(data[0], data[1], data[2]))

        except ConnectionError or ConnectionResetError:
            pass

    def clients_alive(self):
        """
            Sends IS_ALIVE and STATUS_UPD messages to every connected client to check if the
            client is online and to receive it's last status
        """
        while True:
            for client in self.client_list:
                try:
                    if "GUI" not in client.uuid:
                        self.socket_write(client.connection_handler, "IS_ALIVE", client.uuid)
                        self.socket_write(client.connection_handler, "STATUS", client.uuid)
                except Exception:
                    self.remove_client(uuid)
            time.sleep(2.5)


if __name__ == '__main__':
    try:
        server = Server('', 5555, True)
        server.init_socket()

        while True:
            c, i = server.server_socket.accept()

            uuid = server.get_uuid(c)
            y = Node(i[0], i[1], uuid, c)
            server.client_list.append(y)
            if "GUI" in uuid: y.is_gui = True
            server.socket_write(c, "REG_COMPLETE", uuid)

            if server.debug: print(
                "{} - Client with UUID: {}, connected_to_server successfully".format(Server.get_time(), uuid))

            start_new_thread(server.socket_read, (c,))
            start_new_thread(server.clients_alive, ())


    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
