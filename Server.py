"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""

import datetime
import pprint
import socket
import sys
import time

from _thread import *
from Node import Node

import RPi.GPIO as GPIO


class Server:
    def __init__(self, host, port, debug):
        self.host = host
        self.port = port
        self.client_list = []
        self.debug = debug
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.barrier_open = False
        self.operational = True
        self.water_level = self.get_water_level()
        self.status_raspberry1 = self.status_raspberry(0)
        self.status_raspberry2 = self.status_raspberry(1)



        # Define GPIO to LCD mapping
        self.LCD_RS = 7
        self.LCD_E = 8
        self.LCD_D4 = 25
        self.LCD_D5 = 24
        self.LCD_D6 = 23
        self.LCD_D7 = 18

        # Define some device constants
        self.LCD_WIDTH = 16  # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False

        self.LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

    @staticmethod
    def get_time() -> str:
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    def get_water_level(self) -> str:
        for client in self.client_list:
            if "NODE" in self.client_list:
                # Sensor is on 15cm height, minus the distance is the water level
                return "{}cm".format(15 - client.water_level)
        return "Sensor error"

    def lcd_main(self):
        while True:
            try:
                # Main program block
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
                GPIO.setup(self.LCD_E, GPIO.OUT)  # E
                GPIO.setup(self.LCD_RS, GPIO.OUT)  # RS
                GPIO.setup(self.LCD_D4, GPIO.OUT)  # DB4
                GPIO.setup(self.LCD_D5, GPIO.OUT)  # DB5
                GPIO.setup(self.LCD_D6, GPIO.OUT)  # DB6
                GPIO.setup(self.LCD_D7, GPIO.OUT)  # DB7
                GPIO.setup(27, GPIO.IN)  # schakelaar
                GPIO.setup(22, GPIO.IN)  # schakelaar
                GPIO.setup(16, GPIO.IN)  # raspberry 1
                GPIO.setup(12, GPIO.IN)  # raspberry 2

                # Initialise display
                self.lcd_init()

                while True:
                    print(Server.switch_status())
                    # status raspberry
                    if Server.switch_status() == 0:
                        time.sleep(1)
                        if Server.switch_status() == 0:
                            while True:
                                self.lcd_string(self.status_raspberry(0), self.LCD_LINE_1)
                                self.lcd_string(self.status_raspberry(1), self.LCD_LINE_2)
                                if Server.switch_status() != 0:
                                    time.sleep(1)
                                    if Server.switch_status() != 0:
                                        break

                    # status pijl
                    elif Server.switch_status() == 1:
                        time.sleep(1)
                        if Server.switch_status() == 1:
                            while True:
                                self.lcd_string("Water niveau: ", self.LCD_LINE_1)
                                self.lcd_string(str(self.get_water_level()), self.LCD_LINE_2)
                                if Server.switch_status() != 1:
                                    time.sleep(0.5)
                                    if Server.switch_status() != 1:
                                        break
                    elif Server.switch_status() == 2:
                        time.sleep(1)
                        if Server.switch_status() == 2:
                            self.lcd_string("Kering status: ", self.LCD_LINE_1)
                            self.lcd_string("{}".format(self.lcd_kering_status()), self.LCD_LINE_2)
                            if Server.switch_status() != 2:
                                time.sleep(1)
                                if Server.switch_status() != 2:
                                    break
            except KeyboardInterrupt:
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
        """ Formats Node objects toJSON data for all clients in client_list """
        return_string = "{"
        for client in self.client_list:
            return_string = return_string + str(client) + ','
        return_string = return_string[:-1]
        return_string += "}"
        return return_string

    def parse_socket_data(self, data: list) -> str or None:
        """ Handles socket data accordingly, can be either data or a data_header as data type """
        # Check if all data indexes are available
        # data[0 ] == client uuid
        # data[1 ] == data header
        # data[2>] == data
        client = self.find_client(data[0])
        if data[1] == "IS_ALIVE" and data == "ACK":
            client.last_ping = time.time()
        elif data[1] == "BARRIER_STATUS":
            pprint.pprint(data)
        elif data[1] == "UUID":
            return str(data)
        elif data[1] == "GUI_UPDATE_REQ":
            self.socket_write(client.connection_handler, "CLIENT_DATA,{}".format(self.send_client_data()), client.uuid)
        elif data_header == "STATUS_UPDATE_REQ":
            self.socket_write(client.connection_handler, "SERVER_STATUS,{},{},{},{},{}".format(
                                                            str(self.barrier_open),
                                                            str(self.operational),
                                                            str(self.water_level),
                                                            str(self.status_raspberry1),
                                                            str(self.status_raspberry2)),
                                                            client_uuid)

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
        except ConnectionError:
            self.remove_client(client_uuid)

    def socket_read(self, connection):
        """
            Generic function that listens to the connection parameter socket and passes that data
            to the parse_socket_data() function
        """
        while True:
            try:
                data = connection.recv(8192).decode('utf-8').strip().split(',')
                if self.debug: print("{} - Server received: {}".format(Server.get_time(), data))
                try:
                    # Check if all data indexes are available
                    # data[0 ] == client uuid
                    # data[1 ] == data header
                    # data[2>] == data
                    if data[0] or data[1] or data[2]:
                        pass
                except IndexError:
                    continue
                self.parse_socket_data(data)
            except ConnectionError:
                for client in self.client_list:
                    try:
                        self.socket_write(client.connection_handler, "IS_ALIVE", client.uuid)
                    except ConnectionResetError:
                        if "NODE" in client.uuid:
                            client.online = False
                            return
                        self.remove_client(client.uuid)
                        if self.debug:
                            print("{} - Client with UUID {} has lost connection and has been unregistered.".format(
                                Server.get_time(), client.uuid)
                            )
                return

    def get_uuid(self, connection) -> str:
        """ Function is used during client registration to request client for their UUID """
        self.socket_write(connection, "UUID_REQ", "")
        try:
            data = connection.recv(2048).decode('utf-8').strip().split(',')
            return str(self.parse_socket_data(data))

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
                        self.socket_write(client.connection_handler, "STATUS", client.uuid)
                except ConnectionError or ConnectionResetError:
                    self.remove_client(uuid)
            time.sleep(2.5)

    def lcd_kering_status(self) -> str:
        if self.barrier_open:
            return "Geopend"
        else:
            return "Gesloten"

    def status_raspberry(self, x) -> str:
        node_list = []
        for node in self.client_list:
            if "NODE" in node.uuid:
                node_list.append(node)
        if len(node_list) == 0:
            return "{}. Error".format(x+1)
        if node_list[x].online:
            status = "Operationeel"
        else:
            status = "Offline"
        return "{} is {}".format(node_list[x].uuid, status)


    @staticmethod
    def switch_status() -> int:
        if GPIO.input(22):
            return 1
        elif GPIO.input(27):
            return 2
        else:
            return 0

    def lcd_init(self):
        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        GPIO.output(self.LCD_RS, mode)  # RS

        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(self.LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self.LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self.LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        """ Toggle enable """
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        """ Writes string to LCD screen on specified line """
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def is_uuid_in_client_list(self, string: str) -> bool:
        """ Checks if UUID is already registered """
        for client in self.client_list:
            if string == client.uuid:
                return True
        return False


if __name__ == '__main__':
    try:
        server = Server('', 5555, True)
        server.init_socket()

        while True:
            c, i = server.server_socket.accept()

            uuid = server.get_uuid(c)
            y = Node(i[0], i[1], uuid, c)
            if server.is_uuid_in_client_list(uuid):
                y = server.find_client(uuid)
                y.connection_handler = c
                y.online = True
            else:
                server.client_list.append(y)
                if "GUI" in uuid: y.is_gui = True
            server.socket_write(c, "REG_COMPLETE", uuid)

            if server.debug: print(
                "{} - Client with UUID: {}, connected_to_server successfully".format(Server.get_time(), uuid))

            start_new_thread(server.socket_read, (c,))
            start_new_thread(server.clients_alive, ())
            start_new_thread(server.lcd_main, ())

    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
        GPIO.cleanup()
