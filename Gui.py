import csv
import datetime
import json
import math
import pprint
import random
import socket
import time
import tkinter as tk
import tkinter.font
import uuid
from _thread import *
from tkinter import *
from win32api import GetSystemMetrics

import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Node import Node


class Gui(Node, tk.Frame):
    def __init__(self, ip_address: str, port: int, debug: bool):
        # Call super constructors
        super().__init__(
            ip_address=ip_address,
            port=port,
            uuid="GUI-{}".format(uuid.uuid4().hex[:7]),
            connection_handler=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
            debug=debug,
            is_gui=True,
        )

        # Initialise TkInter variables
        self.root = Tk()
        self.font_size_10 = tkinter.font.Font()
        self.font_size_12 = tkinter.font.Font()
        self.hoofd_frame = Frame(self.root)
        self.hoofd_frame_boven = Frame(self.hoofd_frame)
        self.hoofd_frame_midden = Frame(self.hoofd_frame)
        self.hoofd_frame_onder = Frame(self.hoofd_frame)
        self.resultaat_frame = Frame(self.root)
        self.scrollbar = Scrollbar(self.resultaat_frame)
        self.figure = Figure((5, 2), 100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.resultaat_frame)
        self.client_listbox = Listbox(self.hoofd_frame_onder)
        self.boven_frame = Frame(self.root)

        # Initialise TkInter labels
        self.node_1_name_label = Label(master=self.hoofd_frame_boven)
        self.node_1_status_label = Label(master=self.hoofd_frame_boven)
        self.node_2_name_label = Label(master=self.hoofd_frame_midden)
        self.node_2_name_status = Label(master=self.hoofd_frame_midden)
        self.status_label = Label(master=self.boven_frame)
        self.status_value_label = Label(master=self.boven_frame)
        self.barrier_label = Label(master=self.boven_frame)
        self.barrier_value_label = Label(master=self.boven_frame)
        self.water_level_label = Label(master=self.boven_frame)
        self.water_level_value_label = Label(master=self.boven_frame)

        # Initialise and set GUI variables
        self.width = 1000
        self.height = 666
        self.client_list = []
        self.graph_x = []
        self.graph_y = []
        self.bestand_locatie = 'waterpeil.csv'
        self.csv_url = 'https://waterberichtgeving.rws.nl/wbviewer/maak_grafiek.php' \
                       '?loc=HOEK&set=eindverwachting&nummer=1&format=csv'

        # Set TkInter variables
        self.init_tkinter()

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

        # Call TkInter super constructor
        tk.Frame.__init__(self)

    def init_tkinter(self):
        self.font_size_10.configure(family="Courier", size=10)
        self.font_size_12.configure(family="Courier", size=12)

        self.root.title('Status Waterkering')
        self.root.resizable(0, 0)
        self.root.geometry("{}x{}+{}+{}".format(
            self.width,
            self.height,
            int(math.floor(GetSystemMetrics(0)) / 2 - self.width / 2),
            int(math.floor(GetSystemMetrics(1)) / 2 - self.height / 2) - 50)
        )

        self.hoofd_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.hoofd_frame.configure(
            background='DodgerBlue4',
            highlightthickness=15,
            highlightbackground='DodgerBlue4',
            highlightcolor='DodgerBlue4',
        )

        self.hoofd_frame_boven.pack(side=TOP, fill=BOTH, pady=25)
        self.hoofd_frame_boven.configure(
            background='midnight blue',
            highlightthickness=4,
            highlightbackground='black',
            highlightcolor='black'

        )

        self.hoofd_frame_midden.pack(side=TOP, fill=X)
        self.hoofd_frame_midden.configure(
            background='midnight blue',
            highlightthickness=4,
            highlightbackground='black',
            highlightcolor='black'

        )

        self.hoofd_frame_onder.pack(side=BOTTOM, fill=X)
        self.hoofd_frame_onder.configure(background='yellow')

        self.resultaat_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.resultaat_frame.configure(
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

        self.sub_plot = self.figure.add_subplot(111)
        self.sub_plot.plot(self.graph_x[-7:], self.graph_y[-7:])
        self.sub_plot.set_title('Actuele Waterstand ' + Gui.get_time())
        self.sub_plot.set_xlabel('Tijdstip (Afgelopen uur)')
        self.sub_plot.set_ylabel('Verschil NAP in cm')

        self.canvas.show()
        self.canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)  # TODO: Fix access to protected member
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)

        self.client_listbox.config(yscrollcommand=self.scrollbar.set)
        self.client_listbox.pack(side=BOTTOM, fill=BOTH)
        self.client_listbox.configure(
            bd=5,
            font=self.font_size_10,
            height=15,
        )

        self.boven_frame.pack(side=TOP, fill=X)
        self.boven_frame.configure(
            background='midnight blue',
            highlightthickness=15,
            highlightbackground='DodgerBlue4',
            highlightcolor='DodgerBlue4'
        )

        self.node_1_name_label.configure(
            text="Raspberry 1:", bg='midnight blue', fg='white', font=self.font_size_12, height=5)
        self.node_1_status_label.configure(text="Operationeel", bg='midnight blue', fg='green', font=self.font_size_12)
        self.node_1_name_label.grid(row=0, column=0)
        self.node_1_status_label.grid(row=0, column=1)

        self.node_2_name_label.configure(
            text='Raspberry 2:', bg='midnight blue', fg='white', font=self.font_size_12, height=5)
        self.node_2_name_status.configure(text="Inactief", fg='red', bg='midnight blue', font=self.font_size_12)
        self.node_2_name_label.grid(row=0, column=0)
        self.node_2_name_status.grid(row=0, column=1)

        self.status_label.grid(row=0, column=0, sticky=W)
        self.status_value_label.grid(row=0, column=1)
        self.status_label.configure(text="Status:", bg='midnight blue', fg='white', font=self.font_size_12)
        self.status_value_label.configure(text="In werking", bg='midnight blue', fg='white', font=self.font_size_12)

        self.barrier_label.grid(row=1, column=0, sticky=W)
        self.barrier_value_label.grid(row=1, column=1, sticky=W)
        self.barrier_label.configure(text="Kering:", bg='midnight blue', fg='white', font=self.font_size_12)
        self.barrier_value_label.configure(text="OPEN", fg='green', bg='midnight blue', font=self.font_size_12)

        self.water_level_label.grid(row=2, column=0)
        self.water_level_value_label.grid(row=2, column=1, sticky=W)
        self.water_level_label.configure(text="Waterpeil:", bg='midnight blue', fg='white', font=self.font_size_12)
        self.water_level_value_label.configure(text='', fg='white', bg='midnight blue', font=self.font_size_12)

        # TODO: This should work without writing to a file first.
        with open(self.bestand_locatie, 'r') as myCSVFILE:  # Leest het geschreven csv bestand
            reader = csv.reader(myCSVFILE, delimiter=';')
            myCSVFILE.readline()
            for lijn in reader:  # Elke lijn met waardes komt in een tuple
                datum = lijn[0][-5:]
                waterstand = lijn[2]
                if len(waterstand) != 0:
                    self.graph_x.append(datum)
                    self.graph_y.append(int(waterstand))  # Sla de laatste ingevulde waarde van de waterstand op

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    def haal_gegevens_op(self):
        "Haalt gegevens op en schrijft dit weg in een csv bestand"
        with requests.Session() as s:  # Haalt gegevens op van de server
            download = s.get(self.csv_url)

            decoded_content = download.content.decode('utf-8')

            lezen = csv.reader(decoded_content.splitlines(), delimiter=';')
            lijst = list(lezen)

        with open(self.bestand_locatie, 'w', newline='') as myCSVFile:  # Schrijft gegevens weg in csv bestand
            schrijven = csv.writer(myCSVFile, delimiter=';')

            for lijn in lijst:
                schrijven.writerow(lijn)

    def toon_gegevens(self):
        'Zet de gegevens in een listbox met een bijbehorende kleur'
        with open(self.bestand_locatie, 'r') as myCSVFILE:  # Leest het geschreven csv bestand
            self.client_listbox.delete(0, END)
            reader = csv.reader(myCSVFILE, delimiter=';')
            index = 2

            self.client_listbox.insert(0, '{:19}{:15}{:21}{:18}{:4}'.format('Datum/tijd (MET)', '|Astronomisch',
                                                                            '|Gemeten waterstand',
                                                                            '|Verwachte opzet', '|Verwachting RWS'))
            self.client_listbox.insert(1, '{:19}|{:14}|{:20}|{:17}|{:4}'.format('', '', '', '', ''))
            myCSVFILE.readline()

            for lijn in reader:  # Elke lijn met waardes komt in een tuple
                datum = lijn[0]
                astronomisch = lijn[1]
                waterstand = lijn[2]
                opzet = lijn[3]
                verw_RWS = lijn[4]

                self.client_listbox.insert(index,
                                           '{:19}|{:14}|{:20}|{:17}|{:4}'.format(datum, astronomisch, waterstand, opzet,
                                                                                 verw_RWS))
                if int(opzet) >= 30:
                    self.client_listbox.itemconfig(index, {'fg': 'red'})
                elif int(opzet) >= 20 and int(opzet) < 30:
                    self.client_listbox.itemconfig(index, {'fg': 'orange'})
                else:
                    self.client_listbox.itemconfig(index, {'fg': 'green'})

                index += 1

    def parse_socket_data(self, data: str):
        """ Handles socket data accordingly """
        if data[1] == "CLIENT_DATA":
            json_data = ''
            for x in range(2, len(data)):
                json_data += data[x] + ","

            while "},{" in json_data or "{{" in json_data:
                json_data = json_data.replace("},{", "},\"" + str(random.uniform(0, 10)) + "\":{", 1)
                json_data = json_data.replace("{{", "{ \"" + str(random.uniform(0, 10)) + "\":{", 1)
            json_data = json.loads(json_data[:-1])
            self.client_list.clear()

            for x in json_data:
                self.client_list.append(
                    Node(
                        ip_address=json_data[x]['ip_address'],
                        port=int(json_data[x]['port']),
                        uuid=json_data[x]['uuid'],
                        connection_handler=json_data[x]['connection_handler'],
                        barrier_open=bool(json_data[x]['barrier_open']),
                        online=bool(json_data[x]['online']),
                        debug=bool(json_data[x]['debug']),
                        registered=bool(json_data[x]['registered']),
                        is_gui=bool(json_data[x]['is_gui']),
                        last_ping=float(json_data[x]['last_ping'])
                    )
                )
        elif data[1] == "UUID_REQ":
            self.socket_write(data_header="UUID", data=str(self.uuid))
        elif data[1] == "REG_COMPLETE":
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
            if self.debug: print("{} - Connection has been terminated by the server.".format(self.get_time()))
            exit()
        self.connection_handler.send(message.encode('ascii'))

    def socket_read(self):
        """
            Listens to the connection socket of this program instance
            and passes that data to the parse_socket_data() function
        """
        try:
            data = self.connection_handler.recv(4096)
        except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
            if self.debug:
                print("{} - Connection has been terminated by the server.".format(Gui.get_time()))
            sys.exit()
        data = data.decode('utf-8').strip().split(',')
        if self.debug:
            print("{} - GUI received: {}".format(Gui.get_time(), data))
        if (data[0] == self.uuid) or (data[0] == "BROADCAST"):
            return self.parse_socket_data(data=data)

    def button1(self):
        self.client_listbox.delete(0, END)  # Leeg het textveld
        self.populate_client_list()  # Lees de json file en schrijf weg in de listbox
        self.haal_gegevens_op()
        waterpeil = self.graph_y[-1]
        # self.toon_gegevens()
        self.water_level_value_label['text'] = str(waterpeil) + ' cm'
        # self.canvas['plot']= [1,2,3,4,5,6,7], [3,2,5,8,2,6,1]

    def button2(self):
        'Kering sluiten'
        self.barrier_value_label['fg'] = 'red'
        self.barrier_value_label['text'] = 'GESLOTEN'
        # button2['state'] = 'disabled'
        # button3['state'] = 'active'

    def button3(self):
        'Kering openen'
        self.barrier_value_label['fg'] = 'green'
        self.barrier_value_label['text'] = 'OPEN'
        # button3['state'] = 'disabled'
        # button2['state'] = 'active'

    def get_server_data(self):
        """ Sends a request to the server to get the latest client JSON data """
        while True:
            if self.registered:
                self.socket_write("", "GUI_UPDATE_REQ")
                time.sleep(2.5)

    def update_gui(self):
        """  """
        self.populate_client_list()
        self.haal_gegevens_op()
        self.sub_plot.plot(self.graph_x[-35:], self.graph_y[-35:])
        self.water_level_value_label['text'] = str(self.graph_y[-1]) + ' cm'

    def update_gui_handler(self):
        """ Recursively calls update function every x seconds """
        self.update_gui()
        self.root.after(4500, self.update_gui_handler)

    def populate_client_list(self):
        self.client_listbox.delete(0, END)
        self.client_listbox.insert(0, '{:19}{:15}{:21}'.format('UUID', 'IP', 'Port'))

        for client in self.client_list:
            self.client_listbox.insert(2, '{:19}|{:14}|{:20}'.format(client.uuid, client.ip_address, str(client.port)))

    def init_socket_read(self):
        """ socket_read() thread had to be called via another function to work """
        while True:
            self.debug = True
            self.socket_read()


if __name__ == '__main__':
    try:
        gui = Gui("127.0.0.1", 5555, True)
        start_new_thread(gui.get_server_data, ())
        start_new_thread(gui.init_socket_read, ())
        gui.update_gui_handler()
        gui.mainloop()
    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
