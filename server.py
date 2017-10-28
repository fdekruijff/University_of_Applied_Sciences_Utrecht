"""
    Computer Systems and Networks
    University of Applied Sciences Utrecht
    TICT-V1CSN-15 Project
"""

import datetime
import json
import socket
import sys
import time
from _thread import *

from ClientNode import ClientNode

HOST = ''
PORT = 5555
client_list = []
debug = False
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_time():
    """ Returns current time in format %d-%m-%Y %X """
    return datetime.datetime.now().strftime('%d-%m-%Y %X')


def find_client(client_uuid: str) -> ClientNode:
    """ Returns the ClientNode object that matches the passed UUID """
    for x in client_list:
        if client_uuid == x.uuid:
            return x


def remove_client(client_uuid):
    """ Removes a client from the client list, this includes closing the connection handler and updating the status """
    client = find_client(client_uuid)
    if client:
        client.online = False
        client.connection_handler.close()
        client_list.remove(client)
        if debug: print(
            "{} - Client with UUID {} has lost connection and has been unregistered.".format(get_time(), client_uuid))


def send_client_data():
    """ Formats ClientObject parameter JSON data for all clients in client_list """
    return_string = "{"
    for client in client_list:
        return_string = return_string + str(client) + ','
    return_string = return_string[:-1]
    return_string += "}"
    return return_string


def parse_socket_data(client_uuid, data_header, data):
    """ Handles socket data accordingly, can be either data or a data_header as data type """
    client = find_client(client_uuid)
    if data_header == "UUID":
        return data
    if data_header == "ALRM_OFF":
        print("alarm off for uuid" + data)
    elif data_header == "STATUS_UPD":
        json_data = json.loads(data)
        client.ip_address = json_data['ip_address']
        client.port = json_data['port']
        client.uuid = json_data['UUID']
        client.alarm_tripped = json_data['alarm_tripped']
        client.online = json_data['online']
    elif data_header == "IS_ALIVE" and data == "ACK":
        client.online = True
    elif data_header == "ALRM_STATUS":
        client.alarm_status = bool(data)
    elif data_header == "CLIENT_STATUS_UPD":
        client.connection_handler.send(str(str(client.uuid) + ",CLIENT_DATA," + send_client_data()).encode('ascii'))
    elif data_header == "ALRM_TRIP":
        client.alarm_tripped = True
        if debug: print(
            "{} - Client with UUID {} has alarm has been tripped.".format(get_time(), client_uuid))
    elif data_header == "ALRM_CHNG":
        socket_write(client.connection_handler, "ALRM_CHNG", client.uuid)


def socket_write(conn, message: str, client_uuid):
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

    if debug: print("{} - Server send: {}".format(get_time(), message))
    try:
        conn.send(message.encode('ascii'))
    except:
        remove_client(client_uuid)


def socket_read(connection):
    """
        Generic function that listens to the connection parameter socket and passes that data
        to the parse_socket_data() function
    """
    while True:
        try:
            data = connection.recv(4096).decode('utf-8').strip().split(',')
            if debug: print("{} - Server received: {}".format(get_time(), data))
            try:
                if data[0] or data[1] or data[2]:
                    pass
            except IndexError:
                continue
            parse_socket_data(data[0], data[1], data[2])
        except:
            if debug: print("{} - Cannot connect to client".format(get_time()))
            for client in client_list:
                try:
                    socket_write(client.connection_handler, "", "")
                except:
                    if debug: print(
                        "{} - Client with UUID {} has lost connection and has been unregistered.".format(get_time(),
                                                                                                         client.uuid))
                    remove_client(client.uuid)
            return


def get_uuid(connection):
    """ Function is used during client registration to request client for their UUID """
    socket_write(connection, "UUID_REQ", None)
    try:
        data = connection.recv(2048).decode('utf-8').strip().split(',')
        return parse_socket_data(data[0], data[1], data[2])

    except ConnectionError or ConnectionResetError:
        pass


def clients_alive():
    """
        Sends IS_ALIVE and STATUS_UPD messages to every connected client to check if the
        client is online and to receive it's last status
    """
    while True:
        for client in client_list:
            try:
                if "GUI" not in client.uuid:
                    socket_write(client.connection_handler, "IS_ALIVE", client.uuid)
                    socket_write(client.connection_handler, "STATUS_UPD", client.uuid)
            except:
                remove_client(uuid)
        time.sleep(2.5)


if __name__ == '__main__':
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
    except socket.error as e:
        if debug: print("{} - Socket error {}".format(get_time(), e))
        sys.exit()
    finally:
        if debug: print("{} - Successfully bound to socket, PORT:{}".format(get_time(), PORT))

    while True:
        c, i = server_socket.accept()

        uuid = get_uuid(c)
        y = ClientNode(i[0], i[1], uuid, c)
        client_list.append(y)
        if "GUI" in uuid: y.is_gui = True
        socket_write(c, "REG_COMPLETE", uuid)

        if debug: print("{} - Client with UUID: {}, connected_to_server successfully".format(get_time(), uuid))

        start_new_thread(socket_read, (c,))
        start_new_thread(clients_alive, ())
