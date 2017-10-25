import socket
import time
from _thread import *
from ClientNode import ClientNode

HOST = ''
PORT = 5555
client_list = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def parse_data(client_hex, data_header, data):
    if data == "ALRM_TRIP":
        pass
    elif data == "IS_ALIVE":
        socket_write("ACK", client_hex)

    if data_header == "UUID":
        return data
    elif data_header == "STATUS_UPD":
        pass


def socket_is_alive(client_uuid):
    client = None
    for x in client_list:
        if client_uuid == client.uuid:
            client = x

    try:
        while True:
            socket_write("IS_ALIVE", client_uuid)
            data = server_socket.recv(2048).decode('utf-8').strip().split(',')[2]
            if data == "ACK":
                client.online = True
            else:
                client.online = False
                # TODO: do some stuff here
            time.sleep(1)
    finally:
        server_socket.close()


def socket_write(message: str, client_uuid):
    """
        return[0] = Client node UUID
        return[1] = data
    """
    if not client_uuid:
        # Broadcast
        message = "BROADCAST" + "," + message
    else:
        # Unicast
        message = str(client_uuid) + "," + message

    server_socket.send(message.encode('ascii'))


def socket_read(connection):
    try:
        while True:
            data = connection.recv(2048).decode('utf-8').strip().split(',')
            return parse_data(data[0], data[1], data[2])
    finally:
        connection.close()


if __name__ == '__main__':
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
    except socket.error as e:
        print("Socket error {}".format(e))
        exit()
    finally:
        print("Successfully connect to IP:{}, PORT:{}".format(HOST, PORT))

    while True:
        c, i = server_socket.accept()

        socket_write("UUID_REQ", None)
        uuid = socket_read(c)
        client_list.append(ClientNode(i[0], i[1], uuid, c))
        socket_write("REG_COMPLETE", uuid)

        start_new_thread(socket_read, (c,))
