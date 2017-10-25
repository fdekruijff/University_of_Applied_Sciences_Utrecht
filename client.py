import socket
import time
import uuid
from _thread import *

HOST = '192.168.42.2'
PORT = 5555
UUID = uuid.uuid4().hex

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
registered = False
alarm_tripped = False
alarm_enabled = False
alarm_interval_seconds = 5


def parse_data(data: str):
    if data == "REG_COMPLETE":
        registered = True
    elif data == "ALRM_TRIP":
        pass
    elif data == "ALRM_STOP":
        pass
    elif data == "ALRM_ON":
        pass
    elif data == "ALRM_OFF":
        pass
    elif data == "CHNG_INTERVAL":
        pass
    elif data == "IS_ALIVE":
        socket_write("ACK", "")
    elif data == "UUID_REQ":
        socket_write(str(UUID), "UUID")


def socket_write(message: str, data_header: str):
    """
        return[0] = Client node UUID
        return[1] = data_header
        return[2] = data
    """
    message = str(UUID) + "," + data_header + "," + message
    client_socket.send(message.encode('ascii'))


def socket_is_alive():
    global connected
    try:
        while True:
            socket_write("IS_ALIVE", "")
            data = client_socket.recv(2048).decode('utf-8').strip()
            if data == "ACK":
                connected = True
            else:
                connected = False
            time.sleep(1)
    finally:
        client_socket.close()


def socket_read():
    try:
        while True:
            data = client_socket.recv(2048)
            data = data.decode('utf-8').strip().split(',')
            if (data[0] == UUID) or (data[0] == "BROADCAST"):
                return parse_data(data[1])
    finally:
        client_socket.close()


if __name__ == '__main__':
    try:
        client_socket.connect((HOST, PORT))
        connected = True
    except socket.error as e:
        print("Socket error {}".format(e))
        exit()
    finally:
        print("Successfully connect to IP:{}, PORT:{}".format(HOST, PORT))

    while connected:
        start_new_thread(socket_is_alive, ())
        start_new_thread(socket_read, ())
    else:
        print("Not connected anymore!")
