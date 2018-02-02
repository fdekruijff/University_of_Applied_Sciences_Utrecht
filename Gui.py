"""
    Interdisciplinair Project
    University of Applied Sciences Utrecht
    TICT-V1IDP-15 Project
"""

import csv
import datetime
import json
import random
import socket
import time
import tkinter as tk
import tkinter.font
import uuid
import requests

from _thread import *
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Node import Node


# The Gui class is based upon Node and TkInter Frame
class Gui(Node, tk.Frame):
    def __init__(self, ip_address: str, port: int, debug: bool):
        # Call super constructors
        super().__init__(
            ip_address=ip_address,
            port=port,
            uuid="GUI_{}".format(uuid.uuid4().hex[:7]),
            connection_handler=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
            debug=debug,
            is_gui=True,
        )

        # Initialise TkInter objects
        self.root = Tk()
        self.font_size_10 = tkinter.font.Font()
        self.font_size_12 = tkinter.font.Font()
        self.main_frame = Frame(self.root)
        self.top_main_frame = Frame(self.main_frame)
        self.middle_main_frame = Frame(self.main_frame)
        self.under_main_frame = Frame(self.main_frame)
        self.result_frame = Frame(self.root)
        self.scrollbar = Scrollbar(self.under_main_frame)
        self.figure = Figure((5, 2), 100)
        self.sub_plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.result_frame)
        self.client_listbox = Listbox(self.under_main_frame)
        self.top_frame = Frame(self.root)
        self.middle_top_frame = Frame(self.top_frame)

        # Initialise TkInter labels
        self.node_1_name_label = Label(master=self.top_main_frame)
        self.node_1_status_label = Label(master=self.top_main_frame)
        self.node_2_name_label = Label(master=self.middle_main_frame)
        self.node_2_status_label = Label(master=self.middle_main_frame)
        self.status_label = Label(master=self.middle_top_frame)
        self.status_value_label = Label(master=self.middle_top_frame)
        self.barrier_label = Label(master=self.middle_top_frame)
        self.barrier_value_label = Label(master=self.middle_top_frame)
        self.water_level_label = Label(master=self.middle_top_frame)
        self.water_level_value_label = Label(master=self.middle_top_frame)

        # Initialise and set GUI variables
        self.width = 1000
        self.height = 666
        self.client_list = []
        self.graph_x = []
        self.graph_y = []
        self.last_data = None
        self.file_location = 'water_level.csv'
        self.csv_url = 'https://waterberichtgeving.rws.nl/wbviewer/maak_grafiek.php' \
                       '?loc=HOEK&set=eindverwachting&nummer=1&format=csv'

        # Set TkInter variables
        self.set_tkinter_variables()

        # After setting everything up, try to connect to the passed IP and Port
        try:
            self.connection_handler.connect((self.ip_address, self.port))
            self.connected_to_server = True
        except WindowsError:
            if self.debug: print("{} - Could not connect to server, is it running?".format(Gui.get_time()))
            sys.exit()
        except socket.error as e:
            if self.debug: print("{} - Socket error {}".format(Gui.get_time(), e))
            sys.exit()
        if self.debug:
            print("{} - Successfully connect to IP:{}, PORT:{}".format(Gui.get_time(), self.ip_address, self.port))

        # Finally call TkInter super constructor
        tk.Frame.__init__(self)

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    @staticmethod
    def bool(string):
        """ Apparently a bool(str) is always true, so let's use this to convert 'True' to True and 'False' to False """
        if string == "True":
            return True
        return False

    def set_tkinter_variables(self):
        """ Set TkInter variables to the objects created in the constructor """
        self.get_api_data()
        self.read_api_data()
        self.font_size_10.configure(family="Courier", size=10)
        self.font_size_12.configure(family="Courier", size=12)

        self.root.title('Status Waterkering')
        self.root.resizable(0, 0)
        self.root.geometry("{}x{}+{}+{}".format(
            self.width,
            self.height,
            # The auto center functionally to center the frame on your screen doesn't always work, just use 0.
            0,  # int(math.floor(GetSystemMetrics(0)) / 2 - self.width / 2),
            0)  # int(math.floor(GetSystemMetrics(1)) / 2 - self.height / 2) - 50)
        )

        self.main_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.main_frame.configure(
            background='DodgerBlue4',
            highlightthickness=15,
            highlightbackground='DodgerBlue4',
            highlightcolor='DodgerBlue4',
        )

        self.top_main_frame.pack(side=TOP, fill=BOTH)
        self.top_main_frame.configure(
            background='midnight blue',
            highlightthickness=4,
            highlightbackground='black',
            highlightcolor='black'

        )

        self.middle_main_frame.pack(side=TOP, fill=X, pady=25)
        self.middle_main_frame.configure(
            background='midnight blue',
            highlightthickness=4,
            highlightbackground='black',
            highlightcolor='black'

        )

        self.under_main_frame.pack(side=BOTTOM, fill=X)
        self.under_main_frame.configure(background='yellow')

        self.result_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.result_frame.configure(
            width=250,
            height=250,
            background='midnight blue',
            highlightthickness=15,
            highlightbackground='DodgerBlue4',
            highlightcolor='DodgerBlue4'
        )

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.configure(width=25)
        self.scrollbar.config(command=self.client_listbox.yview)

        self.sub_plot.plot(self.graph_x[-7:], self.graph_y[-7:])
        self.sub_plot.set_title('Actuele Waterstand ' + Gui.get_time(), fontsize=10)
        self.sub_plot.set_xlabel('Tijdstip (Afgelopen uur)', fontsize=10)
        self.sub_plot.set_ylabel('Verschil NAP in cm', fontsize=10)

        self.canvas.show()
        self.canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)  # TODO: Fix access to protected member
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)

        self.client_listbox.config(yscrollcommand=self.scrollbar.set)
        self.client_listbox.pack(side=BOTTOM, fill=BOTH)
        self.client_listbox.configure(
            bd=5,
            font=self.font_size_10,
            height=15,
            relief='flat'
        )

        self.top_frame.pack(side=TOP, fill=X)
        self.top_frame.configure(
            background='midnight blue',
            highlightthickness=15,
            highlightbackground='DodgerBlue4',
            highlightcolor='DodgerBlue4'
        )
        self.middle_top_frame.pack(side=TOP, fill=BOTH)
        self.middle_top_frame.configure(
            background='midnight blue',
            highlightthickness=4,
            highlightbackground='black',
            highlightcolor='black'
        )

        self.node_1_name_label.configure(
            text="Raspberry 1:", bg='midnight blue', fg='white', font=self.font_size_12, height=5
        )
        self.node_1_status_label.configure(text='Offline', bg='midnight blue', fg='white', font=self.font_size_12)
        self.node_1_name_label.grid(row=0, column=0)
        self.node_1_status_label.grid(row=0, column=1)

        self.node_2_name_label.configure(
            text='Raspberry 2:', bg='midnight blue', fg='white', font=self.font_size_12, height=5
        )
        self.node_2_status_label.configure(text='Offline', bg='midnight blue', fg='white', font=self.font_size_12)
        self.node_2_name_label.grid(row=0, column=0)
        self.node_2_status_label.grid(row=0, column=1)

        self.status_label.grid(row=0, column=0, sticky=W)
        self.status_value_label.grid(row=0, column=1)
        self.status_label.configure(text="Status:", bg='midnight blue', fg='white', font=self.font_size_12)
        self.status_value_label.configure(text="", bg='midnight blue', fg='white', font=self.font_size_12)

        self.barrier_label.grid(row=1, column=0, sticky=W)
        self.barrier_value_label.grid(row=1, column=1, sticky=W)
        self.barrier_label.configure(text="Kering:", bg='midnight blue', fg='white', font=self.font_size_12)
        self.barrier_value_label.configure(text="Onbekend", fg='white', bg='midnight blue', font=self.font_size_12)

        self.water_level_label.grid(row=2, column=0)
        self.water_level_value_label.grid(row=2, column=1, sticky=W)
        self.water_level_label.configure(text="Waterpeil:", bg='midnight blue', fg='white', font=self.font_size_12)
        self.water_level_value_label.configure(
            text='Sensor error', fg='white', bg='midnight blue', font=self.font_size_12
        )

    def get_api_data(self) -> None:
        """ Get's API data and writes in to CSV file """
        with requests.Session() as s:
            download = s.get(self.csv_url)
            decoded_content = download.content.decode('utf-8')
            result = list(csv.reader(decoded_content.splitlines(), delimiter=';'))

        # Write to file
        with open(self.file_location, 'w', newline='') as myCSVFile:
            write = csv.writer(myCSVFile, delimiter=';')

            for x in result:
                write.writerow(x)

    def read_api_data(self) -> None:
        """ Reads data from CSV file to display in the graph """
        self.graph_x = []
        self.graph_y = []
        with open(self.file_location, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            file.readline()
            for x in reader:  # Every line has a tuple value.
                datum = x[0][-5:]
                water_level = x[2]
                if len(water_level) != 0:
                    self.graph_x.append(datum)
                    self.graph_y.append(int(water_level))

    def parse_socket_data(self, data: list):
        """ Handles socket data accordingly """
        if data[1] == "CLIENT_DATA":
            # Server send a JSON formatted string of all the client data, let's parse it.
            json_data = ''
            for x in range(2, len(data)):
                # Since the socket_read function splits the string based on comma's,
                # we need to stick the string back together
                json_data += data[x] + ","

            # This part fixes some parentheses error when trying to load the JSON
            while "},{" in json_data or "{{" in json_data:
                json_data = json_data.replace("},{", "},\"" + str(random.uniform(0, 10)) + "\":{", 1)
                json_data = json_data.replace("{{", "{ \"" + str(random.uniform(0, 10)) + "\":{", 1)

            # Load the JSON, and remove every current Node in client_list
            json_data = json.loads(json_data[:-1])
            self.client_list.clear()

            for x in json_data:
                if json_data[x]['uuid'] == "NODE_1":
                    # Since NODE_1 holds vital information, like water level and barrier status. We parse it separately
                    self.barrier_open = Gui.bool(json_data[x]['barrier_open'])
                    self.online = Gui.bool(json_data[x]['online'])
                    self.water_level = float(json_data[x]['water_level'])
                    self.water_level_value_label.configure(text=str(round(self.water_level, 1)) + ' cm')

                    # Update the labels while we're at it.
                    if self.online:
                        self.node_1_status_label.configure(text="Online")
                    else:
                        self.node_1_status_label.configure(text="Offline")

                    if self.barrier_open:
                        self.barrier_value_label.configure(text="Open")
                    else:
                        self.barrier_value_label.configure(text="Gesloten")

                # If it's anything else, create a new Node object from the JSON data.
                self.client_list.append(
                    Node(
                        ip_address=json_data[x]['ip_address'],
                        port=int(json_data[x]['port']),
                        uuid=json_data[x]['uuid'],
                        connection_handler=json_data[x]['connection_handler'],
                        barrier_open=Gui.bool(json_data[x]['barrier_open']),
                        online=Gui.bool(json_data[x]['online']),
                        debug=Gui.bool(json_data[x]['debug']),
                        registered=Gui.bool(json_data[x]['registered']),
                        is_gui=Gui.bool(json_data[x]['is_gui']),
                        last_ping=float(json_data[x]['last_ping'])
                    )
                )
        elif data[1] == "UUID_REQ":
            # Server want's to know our UUID, let's write it back to the socket.
            self.socket_write(data_header="UUID", data=str(self.uuid))
        elif data[1] == "REG_COMPLETE":
            # The connection procedure is done.
            self.registered = True

    def socket_write(self, data: str, data_header: str):
        """
            Writes a concatenation of the client UUID, data header and data to
            the connection socket of this program instance
        """
        message = str(self.uuid) + "," + data_header + "," + data
        if self.debug: print("{} - GUI send: {}".format(Gui.get_time(), message))

        try:
            self.connection_handler.send(message.encode('ascii'))
        except ConnectionResetError or ConnectionAbortedError:
            if self.debug:
                print("{} - Connection has been terminated by the server.".format(self.get_time()))
                self.default_values_labels()
        self.connection_handler.send(message.encode('ascii'))

    def socket_read(self):
        """
            Listens to the connection socket of this program instance
            and passes that data to the parse_socket_data() function
        """
        data = ''
        try:
            data = self.connection_handler.recv(8192)
            if data == self.last_data:
                # Don't do anything if data is identical
                return
            self.last_data = data
        except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt or WindowsError:
            if self.debug:
                print("{} - Connection has been terminated by the server.".format(Gui.get_time()))
                self.default_values_labels()
        data = data.decode('utf-8').strip().split(',')
        if self.debug:
            print("{} - GUI received: {}".format(Gui.get_time(), data))
        if (data[0] == self.uuid) or (data[0] == "BROADCAST"):
            return self.parse_socket_data(data=data)

    def default_values_labels(self) -> None:
        """ If the Gui lost connection to the server it will display some default values """
        self.node_1_status_label.configure(text='Offline', bg='midnight blue', fg='white', font=self.font_size_12)
        self.node_2_status_label.configure(text='Offline', bg='midnight blue', fg='white', font=self.font_size_12)
        self.barrier_value_label.configure(text="Onbekend", fg='white', bg='midnight blue', font=self.font_size_12)
        self.water_level_value_label.configure(text='Sensor error', fg='white', bg='midnight blue',
                                               font=self.font_size_12
                                               )
        self.status_value_label.configure(text="Onderhoud vereist", bg='midnight blue', fg='white',
                                          font=self.font_size_12
                                          )
        self.water_level_value_label.configure(text='Sensor error', fg='white', bg='midnight blue',
                                               font=self.font_size_12
                                               )

    def get_server_data(self) -> None:
        """" Sends a request to the server to get the latest client JSON data """
        while True:
            if self.registered:
                self.socket_write("", "GUI_UPDATE_REQ")
                time.sleep(2.5)

    def update_graph(self) -> None:
        """ Function to update the graph """
        self.get_api_data()
        self.graph_y = []
        self.graph_x = []
        self.read_api_data()
        self.sub_plot.set_title('Actuele Waterstand ' + Gui.get_time(), fontsize=10)
        self.canvas.get_tk_widget().forget()
        self.sub_plot.plot(self.graph_x[-7:], self.graph_y[-7:])
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)
        self.canvas.show()

    def nodes_online_check(self) -> None:
        """ Checks if NODE_1 or NODE_2 is online or not and updates labels accordingly """
        node_list = []
        for client in self.client_list:
            if "NODE_1" == client.uuid:
                node_list.append(client.uuid)
            if "NODE_2" == client.uuid:
                node_list.append(client.uuid)

            if "NODE_1" not in node_list:
                self.node_1_status_label['text'] = 'Offline'
            else:
                self.node_1_status_label['text'] = 'Online'

            if "NODE_2" not in node_list:
                self.node_2_status_label['text'] = 'Offline'
            else:
                self.node_2_status_label['text'] = 'Online'

    def update_gui(self):
        """ Function to update labels and the listbox of the GUI """
        self.populate_client_list()
        self.nodes_online_check()

        if self.node_1_status_label['text'] == 'Online' and self.node_2_status_label['text'] == 'Online':
            self.status_value_label['text'] = 'In werking'
        elif self.node_1_status_label['text'] == 'Offline' and self.node_2_status_label['text'] == 'Online':
            self.status_value_label['text'] = 'In werking (onderhoud vereist)'
        elif self.node_2_status_label['text'] == 'Offline' and self.node_1_status_label['text'] == 'Online':
            self.status_value_label['text'] = 'In werking (onderhoud vereist)'
        elif self.node_1_status_label['text'] == 'Offline' and self.node_2_status_label['text'] == 'Offline':
            self.status_value_label['text'] = 'Niet in werking (onderhoud vereist)'

    def update_gui_handler(self):
        """ Recursively calls update function every 4.5 seconds """
        self.update_gui()
        self.root.after(4500, self.update_gui_handler)  # Update gui labels elke 4.5 seconden

    def update_graph_handler(self):
        """ Recursively calls update function every 5 minutes """
        self.update_graph()
        self.root.after(300000, self.update_graph_handler)  # Update grafiek elke 5 minuten

    def populate_client_list(self):
        """ Shows all connected clients in the listbox """
        self.client_listbox.delete(0, END)
        self.client_listbox.insert(0, "{:19}{:15}{:21}".format('UUID', 'IP', 'Port'))
        self.client_listbox.insert(1, '{:19}{:15}{:21}'.format('SERVER_1', '192.168.42.1', '5555'))

        for client in self.client_list:
            self.client_listbox.insert(2, '{:19}{:14}{:20}'.format(client.uuid, client.ip_address, str(client.port)))

    def init_socket_read(self):
        """ socket_read() thread had to be called via another function to work """
        while True:
            self.debug = True
            self.socket_read()


# The main function starts the code.
if __name__ == '__main__':
    try:
        gui = Gui(                                  # Create new Gui object
            str(input("IP: ")),                     # Ask for input, since it depends on how it's setup
            int(input("Port (5555): ")),
            bool(input("Debug (False): "))
        )
        start_new_thread(gui.get_server_data, ())   # Start the tread to ask the server for client data
        start_new_thread(gui.init_socket_read, ())  # Start the thread to listen for server socket traffic
        gui.update_gui_handler()                    # Start the TkInter thread to update the GUI labels
        gui.update_graph_handler()                  # Start the TkInter thread to update the graph
        gui.mainloop()                              # Start TkInter

    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
