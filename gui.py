# GUI Alarmsysteem
import datetime
import socket
import uuid
import time
from _thread import *
from tkinter import *

root = Tk()
serverbool = True
connected_to_server = False
staataan = True
HOST = '192.168.42.1'
PORT = 5555
UUID = "GUI" + uuid.uuid4().hex
debug = True
gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_list = []

informationLabels = ["IP Adres: ", "Port: ", "Action Handler: ", "UUID: "]
informationHeaders = ["General Information", "Events"]
informationContainer = Frame()

root.geometry("{}x{}+400+150".format(800, 500))
root.title("Alarmsysteem")
root.resizable(0, 0)
root.configure(background="#ebedeb")


def parse_socket_data(data: str):
    global connected_to_server
    if data == "UUID_REQ":
        socket_write(str(UUID), "UUID")
        connected_to_server = True


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


def socket_read():
    while True:
        data = None
        try:
            data = gui_socket.recv(4096)
        except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
            if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
            exit()
        data = data.decode('utf-8').strip().split(',')
        if debug: print("{} - GUI received: {}".format(get_time(), data))
        if (data[0] == str(UUID)) or (data[0] == "BROADCAST"):
            return parse_socket_data(data[1])


def button_click():
    global staataan
    staataan = False if staataan else True
    print(staataan)
    if staataan:
        button.configure(bg="red")
        button.configure(text="        Server Disabled         ")
    else:
        button.configure(bg="green")
        button.configure(text="      Alarm Set     ")


def get_client_specifics(x):
    client_input = x.widget.get(x.widget.curselection()[0])
    print(client_input)
    client_info = []
    client = None

    for found_client in client_list:
        if found_client.ip_address.lower() == client_input.lower():
            client = found_client

    client_info.append(client.ip_address)
    client_info.append(client.port)
    client_info.append(client.connection_handler)
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


def get_server_data():
    while True:
        if connected_to_server:
            socket_write("", "CLIENT_STATUS_UPD")
            time.sleep(7.5)

root.informationContainer = Frame()
root.mechanicListBox = Listbox()
root.mechanicListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
root.mechanicListBox.configure(background="white")
root.mechanicListBox.configure(relief=FLAT)
root.mechanicListBox.configure(highlightcolor="#ffffff")
root.mechanicListBox.configure(width=500)
root.mechanicListBox.configure(height=100)
root.mechanicListBox.bind("<Double-Button-1>", get_client_specifics)

# temp
for client in client_list:
    root.mechanicListBox.insert(END, client.ip_address)

button = Button(root, text="      Alarm Set     " if staataan else "      Server Disabled      ", bg="green" if
staataan else "red", command=button_click)
button.grid(row=0, column=0)
button.config(font=("Courier", 11))

label = Label(root,
              text="Status Alarm:\n" + ("ATTENTIE: ER GAAT EEN ALARM AF" if serverbool else "GEEN BIJZONDERHEDEN"))
label.grid(row=0, column=1, padx=300)
label.config(font=("Courier", 11))

if __name__ == '__main__':
    try:
        gui_socket.connect((HOST, PORT))
    except socket.error as e:
        if debug: print("{} - Socket error {}".format(get_time(), e))
        exit()
    finally:
        if debug: print("{} - Successfully connect to IP:{}, PORT:{}".format(get_time(), HOST, PORT))

    start_new_thread(socket_read, ())
    start_new_thread(get_server_data, ())
    mainloop()
