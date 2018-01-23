"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""

import datetime
import socket
import sys
import time
from _thread import *

from Node import Node


class BarrierNode(Node):
    def __init__(self, ip_address: str, port: int, node_name: str, debug: bool):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip_address
        self.port = port
        self.uuid = node_name
        self.is_gui = False
        self.connected_to_server = False
        self.registered = False
        self.debug = debug
        self.last_ping = 0
        self.barrier_open = True

        super().__init__(ip_address, port, node_name, self.client_socket)

    def main_loop(self):
        try:
            try:
                self.client_socket.connect((self.ip_address, self.port))
                self.connected_to_server = True
            except socket.error as e:
                if self.debug: print("{} - Socket error {}".format(BarrierNode.get_time(), e))
                sys.exit()
            finally:
                if self.debug: print(
                    "{} - Successfully connect to IP:{}, PORT:{}".format(
                        BarrierNode.get_time(), self.ip_address, self.port))

            start_new_thread(self.has_timeout, ())

            while True:
                self.socket_read()
        finally:
            self.stop_client()

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    def parse_socket_data(self, data: str):
        """ Handles socket data accordingly """
        if data == "IS_ALIVE":
            self.socket_write(data_header="IS_ALIVE", data="ACK")
            self.last_ping = time.time()
        elif data == "BARRIER_STATUS":
            self.socket_write(data_header="STATUS", data=str(self))
        elif data == "UUID_REQ":
            self.socket_write(data_header="UUID", data=str(self.uuid))

    def socket_write(self, data_header: str, data: str):
        """
            Writes a concatenation of the client UUID, data header and data to
            the connection socket of this program instance
        """
        message = str(self.uuid) + "," + data_header + "," + data
        if self.debug: print("{} - Client send: {}".format(BarrierNode.get_time(), message))

        try:
            self.client_socket.send(message.encode('ascii'))
        except ConnectionResetError or ConnectionAbortedError:
            if self.debug: print("{} - Connection has been terminated by the server.".format(BarrierNode.get_time()))
            self.stop_client()
            sys.exit()
        self.client_socket.send(message.encode('ascii'))

    def stop_client(self):
        """ Cleans up GPIO when exiting """
        # TODO: Cleanup GPIO here
        pass

    def has_timeout(self):
        """ Check if the client is no longer connected if it has not received socket data for more than 5.5 seconds """
        while True:
            time.sleep(1)
            if time.time() - self.last_ping >= 5.5 and self.last_ping != 0:
                if self.debug: print("There is no longer a connection to the server, exiting system")
                self.stop_client()
                sys.exit()

    def socket_read(self):
        """
            Listens to the connection socket of this program instance
            and passes that data to the parse_socket_data() function
        """
        try:
            data = self.client_socket.recv(4096)
        except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
            if self.debug: print("{} - Connection has been terminated by the server.".format(BarrierNode.get_time()))
            self.stop_client()
            sys.exit()
        data = data.decode('utf-8').strip().split(',')
        if self.debug: print("{} - Client received: {}".format(BarrierNode.get_time(), data))
        if (data[0] == self.uuid) or (data[0] == "BROADCAST"):
            return self.parse_socket_data(data=data[1])


if __name__ == '__main__':
    try:
        node = BarrierNode("192.168.137.110", 5555, "test", True)
        node.main_loop()
    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
