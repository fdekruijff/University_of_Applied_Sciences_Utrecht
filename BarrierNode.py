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

import RPi.GPIO as GPIO

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
        self.online = True

        self.afstand = 5096

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.IN)
        GPIO.setup(16, GPIO.IN)
        self.GPIO_TRIGGER = 2
        self.GPIO_ECHO = 3
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

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

            start_new_thread(self.has_timeout, ())

            while True:
                self.socket_read()
        finally:
            BarrierNode.stop_client()

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)  # set Trigger after 0.01ms to LOW
        GPIO.output(self.GPIO_TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            stop_time = time.time()

        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        return ((stop_time - start_time) * 34300) / 2

    def verander_kering_status(self, step_pins: list):
        for pin in step_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        StepCount1 = 4
        Seq1 = list(range(0, StepCount1))
        Seq1[0] = [1, 0, 0, 0]
        Seq1[1] = [0, 1, 0, 0]
        Seq1[2] = [0, 0, 1, 0]
        Seq1[3] = [0, 0, 0, 1]

        StepCount2 = 8
        Seq2 = list(range(0, StepCount2))
        Seq2[0] = [1, 0, 0, 0]
        Seq2[1] = [1, 1, 0, 0]
        Seq2[2] = [0, 1, 0, 0]
        Seq2[3] = [0, 1, 1, 0]
        Seq2[4] = [0, 0, 1, 0]
        Seq2[5] = [0, 0, 1, 1]
        Seq2[6] = [0, 0, 0, 1]
        Seq2[7] = [1, 0, 0, 1]

        Seq = Seq2
        StepCount = StepCount2

        StepCounter = 0
        for rond in range(0, self.afstand):
            for pin in range(0, 4):
                xpin = step_pins[pin]
                if Seq[StepCounter][pin] != 0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            StepCounter += 1
            # Als we aan het einde van de stappenvolgorde zijn beland start dan opnieuw
            if (StepCounter == StepCount): StepCounter = 0
            if (StepCounter < 0): StepCounter = StepCount
            time.sleep(.001)

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    def parse_socket_data(self, data: str):
        """ Handles socket data accordingly """
        if data == "STATUS":
            self.socket_write(data_header="BARRIER_STATUS", data=str(self))
        elif data == "UUID_REQ":
            self.socket_write(data_header="UUID", data=str(self.uuid))
        elif data == "REG_COMPLETE":
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
                self.verander_kering_status([5, 6, 13, 26])
                self.barrier_open = False
            elif self.water_level > 10 and not self.barrier_open:
                self.verander_kering_status([26, 13, 6, 5])
                self.barrier_open = True
            time.sleep(1)

    @staticmethod
    def stop_client():
        """ Cleans up GPIO when exiting """
        GPIO.cleanup()

    def has_timeout(self):
        """ Check if the client is no longer connected if it has not received socket data for more than 5.5 seconds """
        while True:
            self.debug = True
            time.sleep(1)
            if time.time() - self.last_ping >= 5.5 and self.last_ping != 0:
                if self.debug:
                    print("There is no longer a connection to the server, exiting system")
                BarrierNode.stop_client()
                sys.exit()

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
        node = BarrierNode("192.168.42.1", 5555, "NODE_1", True)
        start_new_thread(node.barrier_main_loop, ())
        node.main_loop()
    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
        GPIO.cleanup()
