"""
    Computer Systems and Networks
    University of Applied Sciences Utrecht
    TICT-V1CSN-15 Project
"""

import datetime
import random
import socket
import time
import functools
import uuid
import json

from _thread import *
from ClientNode import ClientNode
from tkinter import *

root = Tk()
server_running = True
connected_to_server = False
alarm_system_is_on = True
HOST = '145.89.96.103'
PORT = 5555
UUID = "GUI" + uuid.uuid4().hex
debug = True
gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_list = []

information_labels = ["IP Adres: ", "Port: ", "Alarm Tripped: ", "UUID: "]
information_headers = ["General Information", "Events"]
information_container = Frame()

root.geometry("{}x{}+400+150".format(800, 500))
root.title("Alarmsysteem")
root.resizable(0, 0)
root.configure(background="#ebedeb")


def parse_socket_data(data: str):
    """ Handles socket data accordingly """
    global connected_to_server
    if data[1] == "UUID_REQ":
        socket_write(str(UUID), "UUID")
        time.sleep(1.5)
        connected_to_server = True
    if data[1] == "CLIENT_DATA":
        json_data = ''
        for x in range(2, len(data)):
            json_data += data[x] + ","

        while "},{" in json_data or "{{" in json_data:
            json_data = json_data.replace("},{", "},\"" + str(random.uniform(0, 10)) + "\":{", 1)
            json_data = json_data.replace("{{", "{ \"" + str(random.uniform(0, 10))+"\":{", 1)
        json_data = json.loads(json_data[:-1])
        client_list.clear()
        for x in json_data:
            ip_address = json_data[x]['ip_address']
            port = json_data[x]['port']
            client_uuid = json_data[x]['uuid']
            alarm_status = json_data[x]['alarm_status']
            alarm_tripped = json_data[x]['alarm_tripped']
            online = json_data[x]['online']
            is_gui = json_data[x]['is_gui']
            client = ClientNode(ip_address, port, client_uuid, None)
            client.alarm_status = alarm_status
            client.alarm_tripped = alarm_tripped
            client.online = online
            client.is_gui = is_gui
            client_list.append(client)


def get_time():
    """ Returns current time in format %d-%m-%Y %X """
    return datetime.datetime.now().strftime('%d-%m-%Y %X')


def socket_write(data: str, data_header: str):
    """
        Writes a concatenation of the client UUID, data header and data to
        the connection socket of this program instance
    """
    message = str(UUID) + "," + data_header + "," + data
    if debug: print("{} - GUI send: {}".format(get_time(), message))

    try:
        gui_socket.send(message.encode('ascii'))
    except ConnectionResetError or ConnectionAbortedError:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        exit()
    gui_socket.send(message.encode('ascii'))


def init_socket_read():
    """ socket_read() thread had to be called via another function to work """
    while True:
        socket_read()


def socket_read():
    """
        Listens to the connection socket of this program instance
        and passes that data to the parse_socket_data() function
    """
    data = None
    try:
        data = gui_socket.recv(4096)
    except ConnectionResetError or ConnectionAbortedError:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        exit()
    data = data.decode('utf-8').strip().split(',')
    if data[0] == '': sys.exit()
    if debug: print("{} - GUI received: {}".format(get_time(), data))
    if (data[0] == str(UUID)) or (data[0] == "BROADCAST"):
        return parse_socket_data(data)


def alarm_system_state_button():
    """ Changes the state of the alarm system """
    global alarm_system_is_on
    alarm_system_is_on = False if alarm_system_is_on else True
    if alarm_system_is_on:
        alarm_state_button.configure(bg="red")
        alarm_state_button.configure(text="    Server Disabled     ")
    else:
        alarm_state_button.configure(bg="green")
        alarm_state_button.configure(text="      Alarm Set  ")


def get_server_data():
    """ Sends a request to the server to get the latest client JSON data """
    while True:
        if connected_to_server:
            socket_write("", "CLIENT_STATUS_UPD")
            time.sleep(7.5)


def update_list_box():
    root.client_list_box.delete(0, END)
    for client in client_list:
        root.client_list_box.insert(END, client.ip_address)


def get_client_specifics(x):
    """ Takes the client_list_box element as input and displays its specifics to the information_container Frame """
    try:
        client_input = x.widget.get(x.widget.curselection()[0])
    except IndexError:
        return
    client_info = []
    client = None

    for found_client in client_list:
        if found_client.ip_address.lower() == client_input.lower():
            client = found_client

    if client:
        client_info.append(client.ip_address)
        client_info.append(client.port)
        client_info.append(client.alarm_tripped)
        client_info.append(client.uuid)

        information_container.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
        information_container.configure(background="white")
        information_container.configure(relief=FLAT)
        information_container.configure(width=500)
        information_container.configure(height=100)

        rely = 0
        for information_text in information_headers:
            information_container.tempLabel = Label(information_container)
            information_container.tempLabel.place(relx=0, rely=rely, relwidth=1, relheight=0.15)
            information_container.tempLabel.configure(text=information_text)
            information_container.tempLabel.configure(background="white")
            information_container.tempLabel.configure(font="Helvetica 12 bold")
            rely += 0.575

        rely = 0.15
        for information_text in range(len(information_labels)):
            information_container.tempLabel = Label(information_container)
            information_container.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
            information_container.tempLabel.configure(background="white")
            information_container.tempLabel.configure(text=information_labels[information_text])
            information_container.tempLabel.configure(anchor='w')

            information_container.tempLabel = Label(information_container)
            information_container.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
            information_container.tempLabel.configure(anchor='w')
            information_container.tempLabel.configure(background="white")
            information_container.tempLabel.configure(text=client_info[information_text])
            rely += 0.085

            information_buttons = Button(information_container)
            information_buttons.place(relx=0.05, rely=0.75, relwidth=0.400)
            information_buttons.configure(anchor='w')
            information_buttons.configure(bg="snow")
            information_buttons.configure(background="white", relief=FLAT)
            information_buttons.configure(text=" Turn off / on ")
            information_buttons.configure(command=functools.partial(socket_write, client.uuid, "ALRM_CHNG"))

            information_buttons = Button(information_container)
            information_buttons.place(relx=0.5, rely=0.75, relwidth=0.400)
            information_buttons.configure(anchor='w')
            information_buttons.configure(bg="white", relief=FLAT)
            if alarm_system_is_on:
                information_buttons.configure(text="The Alarm is turned on")
            else:
                information_buttons.configure(text="The Alarm is turned off")


def init_gui_elements():
    """ Initialises default elements for TkInter Gui frame """
    root.client_list_box = Listbox()
    root.client_list_box.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
    root.client_list_box.configure(background="white")
    root.client_list_box.configure(relief=FLAT)
    root.client_list_box.configure(highlightcolor="#ffffff")
    root.client_list_box.configure(width=500)
    root.client_list_box.configure(height=100)
    root.client_list_box.bind("<Double-Button-1>", get_client_specifics)

    alarm_state_button.configure(bg="green" if alarm_system_is_on else "red")
    alarm_state_button.configure(text="   Alarm Set   " if alarm_system_is_on else "Server Disabled")
    alarm_state_button.configure(command=alarm_system_state_button)
    alarm_state_button.grid(row=0, column=0)
    alarm_state_button.config(font=("Courier", 11))

    alarm_state_label.configure(
        text="Status Alarm:\n" + ("ATTENTIE: ER GAAT EEN ALARM AF" if server_running else "GEEN BIJZONDERHEDEN"))
    alarm_state_label.grid(row=0, column=1, padx=300)
    alarm_state_label.config(font=("Courier", 11))


def client_list_box_update():
    """ Recursively recalled to update the client data in the list box based on the data received from the server """
    update_list_box()
    root.after(2000, client_list_box_update)


if __name__ == '__main__':
    try:
        gui_socket.connect((HOST, PORT))
    except socket.error as e:
        if debug: print("{} - Socket error {}".format(get_time(), e))
        exit()
    finally:
        if debug: print("{} - Successfully connect to IP:{}, PORT:{}".format(get_time(), HOST, PORT))

    alarm_state_label = Label(root)
    alarm_state_button = Button(root)
    root.informationContainer = Frame()

    start_new_thread(get_server_data, ())
    start_new_thread(init_socket_read, ())
    client_list_box_update()
    mainloop()
