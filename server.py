import datetime
import socket
import time
from _thread import *

from ClientNode import ClientNode

HOST = ''
PORT = 5555
client_list = []
debug = True
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_time():
    return datetime.datetime.now().strftime('%d-%m-%Y %X')


def find_client(client_uuid: str) -> ClientNode:
    for x in client_list:
        if client_uuid == x.uuid:
            return x


def parse_socket_data(client_uuid, data_header, data):
    client = find_client(client_uuid)
    if data == "ALRM_TRIP":
        client.alarm_tripped = True

    if data_header == "UUID":
        return data
    elif data_header == "STATUS_UPD":
        pass
    elif data_header == "IS_ALIVE" and data == "ACK":
        client.online = True


def socket_write(conn, message: str, client_uuid):
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

    if debug: print("{} - Server send: {}".format(get_time(), message))
    try:
        conn.send(message.encode('ascii'))
    except ConnectionAbortedError:
        client = find_client(client_uuid)
        client.online = False
        client.connection_handler.close()
        client_list.remove(client)
        if debug: print(
            "{} - Client with UUID {} has lost connection and has been unregistered.".format(get_time(), client_uuid))


def socket_read(connection):
    while True:
        data = connection.recv(2048).decode('utf-8').strip().split(',')
        if debug: print("{} - Server received: {}".format(get_time(), data))
        parse_socket_data(data[0], data[1], data[2])


def get_uuid(connection):
    socket_write(connection, "UUID_REQ", None)
    data = connection.recv(2048).decode('utf-8').strip().split(',')
    return parse_socket_data(data[0], data[1], data[2])


def clients_alive():
    while True:
        for client in client_list:
            socket_write(client.connection_handler, "IS_ALIVE", client.uuid)
        time.sleep(2.5)


if __name__ == '__main__':
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
    except socket.error as e:
        if debug: print("{} - Socket error {}".format(get_time(), e))
        exit()
    finally:
        if debug: print("{} - Successfully bound to socket, PORT:{}".format(get_time(), PORT))

    while True:
        c, i = server_socket.accept()

        uuid = get_uuid(c)
        client_list.append(ClientNode(i[0], i[1], uuid, c))
        socket_write(c, "REG_COMPLETE", uuid)
        if debug: print("{} - Client with UUID: {}, connected successfully".format(get_time(), uuid))

        start_new_thread(socket_read, (c,))
        start_new_thread(clients_alive, ())
