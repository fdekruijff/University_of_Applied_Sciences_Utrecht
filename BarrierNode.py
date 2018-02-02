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

import RPi.GPIO as GPIO


# The class BarrierNode extends the class Node
class BarrierNode(Node):
    def __init__(self, ip_address: str, port: int, node_name: str, debug: bool):
        # Set the super variables (Node.py)
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
        self.online = True

        # Set DC motor distance to close the barrier
        self.door_distance = 5096

        # Set GPIO settings and pins
        self.GPIO_TRIGGER = 2
        self.GPIO_ECHO = 3
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.IN)
        GPIO.setup(16, GPIO.IN)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        # Call super Node super constructor
        super().__init__(ip_address, port, node_name, self.client_socket)

    def main_loop(self):
        try:
            try:
                self.client_socket.connect((self.ip_address, self.port))
                self.connected_to_server = True
            except socket.error as e:
                if self.debug:
                    print("{} - Socket error {}".format(BarrierNode.get_time(), e))
                sys.exit()
            finally:
                if self.debug:
                    print(
                        "{} - Successfully connect to IP:{}, PORT:{}".format(
                            BarrierNode.get_time(), self.ip_address, self.port))

            while True:
                self.socket_read()
        finally:
            BarrierNode.stop_client()

    def distance(self) -> float:
        """ Returns the sonic sensor distance """
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)  # set Trigger after 0.01ms to LOW
        GPIO.output(self.GPIO_TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        # save start_time
        while GPIO.input(self.GPIO_ECHO) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            stop_time = time.time()

        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        return float(((stop_time - start_time) * 34300) / 2)

    def change_barrier_status(self, step_pins: list):
        for pin in step_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        step_count1 = 4
        seq1 = list(range(0, step_count1))
        seq1[0] = [1, 0, 0, 0]
        seq1[1] = [0, 1, 0, 0]
        seq1[2] = [0, 0, 1, 0]
        seq1[3] = [0, 0, 0, 1]

        step_count2 = 8
        seq2 = list(range(0, step_count2))
        seq2[0] = [1, 0, 0, 0]
        seq2[1] = [1, 1, 0, 0]
        seq2[2] = [0, 1, 0, 0]
        seq2[3] = [0, 1, 1, 0]
        seq2[4] = [0, 0, 1, 0]
        seq2[5] = [0, 0, 1, 1]
        seq2[6] = [0, 0, 0, 1]
        seq2[7] = [1, 0, 0, 1]

        seq = seq2
        step_count = step_count2

        step_counter = 0
        for x in range(0, self.door_distance):
            for pin in range(0, 4):
                x_pin = step_pins[pin]
                if seq[step_counter][pin] != 0:
                    GPIO.output(x_pin, True)
                else:
                    GPIO.output(x_pin, False)

            step_counter += 1
            # When we reach the end of the step order, we start over
            if step_counter == step_count:
                step_counter = 0
            if step_counter < 0:
                step_counter = step_count
            time.sleep(.001)

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    @staticmethod
    def stop_client():
        """ Cleans up GPIO when stopping the program """
        GPIO.cleanup()

    def parse_socket_data(self, data: str):
        """ Handles socket data accordingly """
        if data == "STATUS":
            # Server is asking for a status update, return a string of self (overrides __str__ in Node.py)
            self.socket_write(data_header="BARRIER_STATUS", data=str(self))
        elif data == "UUID_REQ":
            # Server want's to know our UUID, let's write it back to the socket.
            self.socket_write(data_header="UUID", data=str(self.uuid))
        elif data == "REG_COMPLETE":
            # The connection procedure is done.
            self.online = True
            self.registered = True

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
            if self.debug:
                print("{} - Connection has been terminated by the server.".format(BarrierNode.get_time()))
            BarrierNode.stop_client()
            sys.exit()
        self.client_socket.send(message.encode('ascii'))

    def barrier_main_loop(self):
        """ Opens or closes barrier based on water level """
        while True:
            self.water_level = self.distance()
            if self.water_level <= 10 and self.barrier_open:
                self.change_barrier_status([5, 6, 13, 26])
                self.barrier_open = False
            elif self.water_level > 10 and not self.barrier_open:
                self.change_barrier_status([26, 13, 6, 5])
                self.barrier_open = True
            time.sleep(1)

    def socket_read(self):
        """
            Listens to the connection socket of this program instance
            and passes that data to the parse_socket_data() function
        """
        try:
            data = self.client_socket.recv(8192)
        except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
            if self.debug:
                print("{} - Connection has been terminated by the server.".format(BarrierNode.get_time()))
            BarrierNode.stop_client()
            sys.exit()
        data = data.decode('utf-8').strip().split(',')
        if self.debug:
            print("{} - Client received: {}".format(BarrierNode.get_time(), data))
        if (data[0] == self.uuid) or (data[0] == "BROADCAST"):
            return self.parse_socket_data(data=data[1])


if __name__ == '__main__':
    try:
        node = BarrierNode(                             # Create new BarrierNode object
            str(input("IP: ")),                         # Ask for input, since it depends on how it's setup
            int(input("Port (5555): ")),
            str(input("UUID (NODE_1 | NODE_2): ")),
            bool(input("Debug (False): "))
        )

        start_new_thread(node.barrier_main_loop, ())    # Start the barrier main loop in a thread
        node.main_loop()                                # Start the socket main loop in a thread
    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
        GPIO.cleanup()
