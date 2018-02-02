"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""

import datetime
import json
import socket
import sys
import time

from _thread import *
from Node import Node

import RPi.GPIO as GPIO


class Server:
    def __init__(self, host, port, debug):
        # Define super variables.
        self.host = host
        self.port = port
        self.debug = debug
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define Server variables.
        self.barrier_open = False
        self.operational = True
        self.client_list = []

        # Define GPIO to LCD mapping.
        self.LCD_RS = 7
        self.LCD_E = 8
        self.LCD_D4 = 25
        self.LCD_D5 = 24
        self.LCD_D6 = 23
        self.LCD_D7 = 18

        # Define some device constants.
        self.LCD_WIDTH = 16  # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False
        self.LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

    @staticmethod
    def get_time() -> str:
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    @staticmethod
    def switch_status() -> int:
        """ Returns the switch status for the LCD screen """
        if GPIO.input(22):
            return 1
        elif GPIO.input(27):
            return 2
        else:
            return 0

    @staticmethod
    def bool(string):
        """ Apparently a bool(str) is always true, so let's use this to convert 'True' to True and 'False' to False """
        if string == "True":
            return True
        return False

    def get_water_level(self) -> str:
        """ Returns water level as recorded by NODE_1 """
        for client in self.client_list:
            if "NODE_1" in client.uuid:
                return "{}cm".format(round(client.water_level, 1))
        return "Sensor error"

    def lcd_main(self):
        """ Thread that handles LCD logic, based on physical switch """
        while True:
            try:
                # Main program block.
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
                GPIO.setup(self.LCD_E, GPIO.OUT)   # E
                GPIO.setup(self.LCD_RS, GPIO.OUT)  # RS
                GPIO.setup(self.LCD_D4, GPIO.OUT)  # DB4
                GPIO.setup(self.LCD_D5, GPIO.OUT)  # DB5
                GPIO.setup(self.LCD_D6, GPIO.OUT)  # DB6
                GPIO.setup(self.LCD_D7, GPIO.OUT)  # DB7
                GPIO.setup(27, GPIO.IN)  # Switch
                GPIO.setup(22, GPIO.IN)  # Switch
                GPIO.setup(16, GPIO.IN)  # Raspberry 1
                GPIO.setup(12, GPIO.IN)  # Raspberry 2

                # Initialise display.
                self.lcd_init()

                while True:
                    # Display the status of client node Raspberry Pi's on the LCD.
                    if Server.switch_status() == 0:
                        time.sleep(1)
                        if Server.switch_status() == 0:
                            while True:
                                self.status_raspberry()
                                if Server.switch_status() != 0:
                                    time.sleep(1)
                                    if Server.switch_status() != 0:
                                        break

                    # Display the water level on the LCD.
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
                    # Display the barrier status on the LCD.
                    elif Server.switch_status() == 2:
                        time.sleep(1)
                        if Server.switch_status() == 2:
                            self.lcd_string("Kering status: ", self.LCD_LINE_1)
                            self.lcd_string("{}".format(self.lcd_barrier_status()), self.LCD_LINE_2)
                            if Server.switch_status() != 2:
                                time.sleep(1)
                                if Server.switch_status() != 2:
                                    break
            # Sometimes the switch crashes this code, just loop again and continue.
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

    def find_client_obj(self, client_uuid: str) -> Node or None:
        """ Returns the Node object that matches the passed UUID, or None of no Node has been found """
        for x in self.client_list:
            if client_uuid == x.uuid:
                return x
        return None

    def find_client_bool(self, string: str) -> bool:
        """ Returns bool instead of Node object """
        for client in self.client_list:
            if string == client.uuid:
                return True
        return False

    def remove_client(self, client_uuid: str) -> None:
        """
            Removes a client from the client list, this includes closing the connection handler and updating the status
        """
        client = self.find_client_obj(client_uuid)
        if client:
            self.client_list.remove(client)
            if self.debug:
                print("{} - Client with UUID {} has lost connection and has been unregistered.".format(
                    Server.get_time(), client_uuid))

    def send_client_data(self) -> str:
        """ Formats Node objects to JSON data for all clients in client_list, to send over sockets """
        return_string = "{"
        for client in self.client_list:
            return_string = return_string + str(client) + ','
        # Remove the last comma, because it's the last object in the JSON list.
        return_string = return_string[:-1]
        # Finish up JSON syntax.
        return_string += "}"
        return return_string

    def parse_socket_data(self, data: list) -> str or None:
        """ Handles socket data accordingly, data contains some handle information as shown below """
        # What each data element represents.
        # data[0 ] == client uuid
        # data[1 ] == data header
        # data[2>] == data

        # Fetch the Node object.
        client = self.find_client_obj(data[0])

        # Load JSON object.
        if data[1] == "BARRIER_STATUS":
            json_data = ''
            for x in range(2, len(data)):
                json_data += data[x] + ","
            json_data = json.loads(json_data[:-1])
            client = self.find_client_obj(json_data['uuid'])
            # Check if this node is already registered.
            if client:
                # A client object has been returned.
                client.online = Server.bool(json_data['online'])
                client.barrier_open = Server.bool(json_data['barrier_open'])
                client.registered = Server.bool(json_data['registered'])
                client.water_level = float(json_data['water_level'])
        elif data[1] == "UUID":
            # This is for the registration of a new client, client just supplied their UUID. Pass it along.
            return str(data[0])
        elif data[1] == "GUI_UPDATE_REQ":
            # GUI asks for an update request, send along a JSON version of the client list.
            self.socket_write(client.connection_handler, "CLIENT_DATA,{}".format(self.send_client_data()), client.uuid)

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
                        # This vital piece of code let's the Nodes reconnect if they lost connection.
                        # Their object remain in the client_list, but they are set to offline. When they reconnect
                        # they are only reset to online, and the connection_handler is update.
                        if "NODE" in client.uuid:
                            client.online = False
                            return
                        self.remove_client(client.uuid)
                        if self.debug:
                            print("{} - Client with UUID {} has lost connection and has been unregistered.".format(
                                Server.get_time(), client.uuid))

    def get_uuid(self, connection) -> str:
        """ Function is used during client registration to request client for their UUID """
        # Send UUID Request to the client
        self.socket_write(connection, "UUID_REQ", "")
        try:
            # Let the parse socket data function handle the response, as it probably contains the UUID.
            data = connection.recv(2048).decode('utf-8').strip().split(',')
            return str(self.parse_socket_data(data))
        # Handle some errors if thrown, but don't do anything with it.
        except ConnectionError or ConnectionResetError:
            pass

    def recursive_client_calls(self):
        """
            Recursively sends data headers to Node clients in client_list
        """
        while True:
            for client in self.client_list:
                try:
                    if "GUI" not in client.uuid:
                        # If it's not a GUI, ask the Node for a status update.
                        self.socket_write(client.connection_handler, "STATUS", client.uuid)
                except ConnectionError or ConnectionResetError:
                    # The connection failed, remove the client from the list.
                    self.remove_client(uuid)
            time.sleep(2.5)

    def lcd_barrier_status(self) -> str:
        """ NODE_1 decides if the Barrier should be opened or closed """
        for client in self.client_list:
            if client.uuid == "NODE_1":
                if client.barrier_open:
                    return "Geopend"
                return "Gesloten"
        return "Onbekend"

    def status_raspberry(self) -> None:
        """ Updates LCD line 1 and 2 accordingly if the NODE Raspberry Pi's are online or not """
        status_1 = "1.Niet verbonden"
        status_2 = "2.Niet verbonden"
        for client in self.client_list:
            if "NODE_1" in client.uuid:
                if client.online:
                    status_1 = "1.Operationeel"
                else:
                    status_1 = "1.Niet verbonden"
            if "NODE_2" in client.uuid:
                if client.online:
                    status_2 = "2.Operationeel"
                else:
                    status_2 = "2.Niet verbonden"
        self.lcd_string(status_1, self.LCD_LINE_1)
        self.lcd_string(status_2, self.LCD_LINE_2)

    def lcd_init(self) -> None:
        """ Default code to initialise the LCD screen """
        self.lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode) -> None:
        """ Default code to display text to the LCD """
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

    def lcd_toggle_enable(self) -> None:
        """ Toggle enable in LCD register """
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line) -> None:
        """ Writes string to LCD screen on specified line """
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(line, self.LCD_CMD)

        for pixel in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[pixel]), self.LCD_CHR)


# The main function starts the code.
if __name__ == '__main__':
    try:
        server = Server('', 5555, True)           # Create new Server object.
        server.init_socket()                      # Bring the socket online.
        start_new_thread(server.lcd_main, ())     # Start the LCD in a tread.

        while True:
            c, i = server.server_socket.accept()  # The interpreter waits here until a client connects.

            uuid = server.get_uuid(c)             # Some socket traffic is exchanged to identify the UUID.
            y = Node(i[0], i[1], uuid, c)         # There is a new Node object created for the connected client.
            if server.find_client_bool(uuid):     # If a Node reconnects, update the existing object in client_list.
                y = server.find_client_obj(uuid)
                y.connection_handler = c
                y.online = True
            else:
                server.client_list.append(y)
                if "GUI" in uuid: y.is_gui = True
            server.socket_write(c, "REG_COMPLETE", uuid) # If the connection procedure is done, notify the client.

            if server.debug: print(
                "{} - Client with UUID: {}, connected_to_server successfully".format(Server.get_time(), uuid))

            # For each client the following threads are started.
            start_new_thread(server.socket_read, (c,))
            start_new_thread(server.recursive_client_calls, ())

    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
        GPIO.cleanup()
