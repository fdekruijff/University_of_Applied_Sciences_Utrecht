# GUI Alarmsysteem
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
serverbool = True
connected_to_server = False
staataan = True
HOST = '145.89.96.103'
PORT = 5555
UUID = "GUI" + uuid.uuid4().hex
debug = True
gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_list = []

informationLabels = ["IP Adres: ", "Port: ", "Alarm Tripped: ", "UUID: "]
informationHeaders = ["General Information", "Events"]
informationContainer = Frame()

root.geometry("{}x{}+400+150".format(800, 500))
root.title("Alarmsysteem")
root.resizable(0, 0)
root.configure(background="#ebedeb")


def parse_socket_data(data: str):
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
        ip_address, port, uuid, alarm_tripped, alarm_tripped, online, is_gui = "", "", "", "", "", "", ""
        client_list.clear()
        for x in json_data:
            ip_address = json_data[x]['ip_address']
            port = json_data[x]['port']
            uuid = json_data[x]['uuid']
            alarm_status = json_data[x]['alarm_status']
            alarm_tripped = json_data[x]['alarm_tripped']
            online = json_data[x]['online']
            is_gui = json_data[x]['is_gui']
            client = ClientNode(ip_address, port, uuid, None)
            client.alarm_status = alarm_status
            client.alarm_tripped = alarm_tripped
            client.online = online
            client.is_gui = is_gui
            client_list.append(client)




def get_time():
    return datetime.datetime.now().strftime('%d-%m-%Y %X')


def socket_write(data: str, data_header: str):
    """
        return[0] = Client node UUID
        return[1] = data_header
        return[2] = data
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
    while True:
        socket_read()


def socket_read():
    # while True:
    data = None
    try:
        data = gui_socket.recv(4096)
    except ConnectionResetError or ConnectionAbortedError:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        exit()
    data = data.decode('utf-8').strip().split(',')
    if debug: print("{} - GUI received: {}".format(get_time(), data))
    if (data[0] == str(UUID)) or (data[0] == "BROADCAST"):
        return parse_socket_data(data)


def button_click():
    global staataan
    staataan = False if staataan else True
    if staataan:
        button.configure(bg="red")
        button.configure(text="        Server Disabled         ")
    else:
        button.configure(bg="green")
        button.configure(text="      Alarm Set     ")


def get_client_specifics(x):
    client_input = x.widget.get(x.widget.curselection()[0])
    client_info = []
    client = None

    for found_client in client_list:
        if found_client.ip_address.lower() == client_input.lower():
            client = found_client

    client_info.append(client.ip_address)
    client_info.append(client.port)
    client_info.append(client.alarm_tripped)
    client_info.append(client.uuid)

    informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
    informationContainer.configure(background="white")
    informationContainer.configure(relief=FLAT)
    informationContainer.configure(width=500)
    informationContainer.configure(height=100)

    rely = 0
    for label in informationHeaders:
        informationContainer.tempLabel = Label(informationContainer)
        informationContainer.tempLabel.place(relx=0, rely=rely, relwidth=1, relheight=0.15)
        informationContainer.tempLabel.configure(text=label)
        informationContainer.tempLabel.configure(background="white")
        informationContainer.tempLabel.configure(font="Helvetica 12 bold")

        rely += 0.575

    rely = 0.15
    for label in range(len(informationLabels)):
        informationContainer.tempLabel = Label(informationContainer)
        informationContainer.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
        informationContainer.tempLabel.configure(background="white")
        informationContainer.tempLabel.configure(text=informationLabels[label])
        informationContainer.tempLabel.configure(anchor='w')

        informationContainer.tempLabel = Label(informationContainer)
        informationContainer.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
        informationContainer.tempLabel.configure(anchor='w')
        informationContainer.tempLabel.configure(background="white")
        informationContainer.tempLabel.configure(text=client_info[label])
        rely += 0.085

        tempLabel1 = Button(informationContainer)
        tempLabel1.place(relx=0.05, rely=0.75, relwidth=0.400)
        tempLabel1.configure(anchor='w')
        tempLabel1.configure(bg="snow")
        # tempLabel.configure()
        tempLabel1.configure(background="white", relief=FLAT)
        tempLabel1.configure(text=" Turn off / on ")
        tempLabel1.configure(command=functools.partial(socket_write, client.uuid, "ALRM_OFF"))

        tempLabel = Label(informationContainer)
        tempLabel.place(relx=0.5, rely=0.75, relwidth=0.400)
        tempLabel.configure(anchor='w')
        tempLabel.configure(bg="white", relief=FLAT)
        tempLabel1.configure(command=functools.partial(socket_write, client.uuid, "ALRM_CHNG"))
        if staataan:
            tempLabel.configure(text="The Alarm is turned on")
        else:
            tempLabel.configure(text="The Alarm is turned off")


def get_server_data():
    while True:
        if connected_to_server:
            socket_write("", "CLIENT_STATUS_UPD")
            time.sleep(7.5)


def update_list_box():
    root.client_list_box.delete(0, END)
    for client in client_list:
        root.client_list_box.insert(END, client.ip_address)


root.informationContainer = Frame()
root.client_list_box = Listbox()
root.client_list_box.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
root.client_list_box.configure(background="white")
root.client_list_box.configure(relief=FLAT)
root.client_list_box.configure(highlightcolor="#ffffff")
root.client_list_box.configure(width=500)
root.client_list_box.configure(height=100)
root.client_list_box.bind("<Double-Button-1>", get_client_specifics)

button = Button(root, text="      Alarm Set     " if staataan else "      Server Disabled      ", bg="green" if
staataan else "red", command=button_click)
button.grid(row=0, column=0)
button.config(font=("Courier", 11))

label = Label(root,
              text="Status Alarm:\n" + ("ATTENTIE: ER GAAT EEN ALARM AF" if serverbool else "GEEN BIJZONDERHEDEN"))
label.grid(row=0, column=1, padx=300)
label.config(font=("Courier", 11))


def update():
    update_list_box()
    root.after(2000, update)


if __name__ == '__main__':
    try:
        gui_socket.connect((HOST, PORT))
    except socket.error as e:
        if debug: print("{} - Socket error {}".format(get_time(), e))
        exit()
    finally:
        if debug: print("{} - Successfully connect to IP:{}, PORT:{}".format(get_time(), HOST, PORT))

    start_new_thread(get_server_data, ())
    start_new_thread(init_socket_read, ())
    update()
    mainloop()
