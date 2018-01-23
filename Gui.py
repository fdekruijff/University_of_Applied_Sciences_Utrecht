import csv
import requests
import tkinter.font
import uuid
import datetime
import socket
import time

from tkinter import *
import tkinter as tk
from _thread import *
from Node import Node


class Gui(Node, tk.Frame):
    def __init__(self, ip_address: str, port: int, debug: bool):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip_address
        self.port = port
        self.uuid = "GUI-{}".format(uuid.uuid4().hex[:7])
        self.is_gui = True
        self.connected_to_server = False
        self.registered = False
        self.debug = debug
        self.last_ping = 0
        self.barrier_open = None

        self.bestand_locatie = 'waterpeil.csv'
        self.csv_url = 'https://waterberichtgeving.rws.nl/wbviewer/maak_grafiek.php' \
                       '?loc=HOEK&set=eindverwachting&nummer=1&format=csv'

        self.init_tkinter()

        tk.Frame.__init__(self)
        super().__init__(ip_address, 5555, self.uuid, self.client_socket)

    def init_tkinter(self):
        self.root = Tk()

        self.my_font = tkinter.font.Font(family="Courier", size=9)
        self.my_font2 = tkinter.font.Font(family="Courier", size=12)

        self.root.resizable(width=False, height=False)
        self.root.minsize(width=800, height=600)
        self.root.maxsize(width=800, height=600)

        self.hoofdframe = Frame(master=self.root,  # Maakt hoofdframe aan
                           background='midnight blue',
                           highlightthickness=15,
                           highlightbackground='DodgerBlue4',
                           highlightcolor='DodgerBlue4'
                           )
        self.hoofdframe.pack(side=LEFT, fill=BOTH, expand=True)

        self.resultaatframe = Frame(master=self.root,  # Maakt resultaatframe aan
                               width=250,
                               height=250,
                               background='midnight blue',
                               highlightthickness=15,
                               highlightbackground='DodgerBlue4',
                               highlightcolor='DodgerBlue4'
                               )
        self.resultaatframe.pack(side=BOTTOM)

        self.scrollbar = Scrollbar(master=self.resultaatframe, width=25)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.button1 = Button(master=self.resultaatframe, text='VERVERS GEGEVENS', command=self.button1)
        self.button1.pack(side=BOTTOM, fill=X)

        self.textVeld = Listbox(master=self.resultaatframe,  # Listbox om resultaten csv weer te geven
                           bd=5,
                           width=55,
                           font=self.my_font,
                           height=26,
                           )

        self.textVeld.pack(side=BOTTOM)

        self.bovenframe = Frame(master=self.root,  # Maakt resultaatframe aan
                           background='midnight blue',
                           highlightthickness=15,
                           highlightbackground='DodgerBlue4',
                           highlightcolor='DodgerBlue4'
                           )
        self.bovenframe.pack(side=TOP, fill=BOTH, expand=True)

        self.textVeld.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.textVeld.yview)

        self.label7 = Label(master=self.hoofdframe, text="Raspberry 1:", bg='midnight blue', fg='white', font=self.my_font2)
        self.label7.grid(row=0, column=0)

        self.label8 = Label(master=self.hoofdframe, text="Operationeel", bg='midnight blue', fg='white', font=self.my_font2)
        self.label8.grid(row=1, column=0)

        self.label9 = Label(master=self.hoofdframe, text='', bg='midnight blue', fg='white', font=self.my_font2)
        self.label9.grid(row=2, column=0)

        self.label10 = Label(master=self.hoofdframe, text='Raspberry 2:', bg='midnight blue', fg='white', font=self.my_font2)
        self.label10.grid(row=3, column=0)

        self.label11 = Label(master=self.hoofdframe, text="Operationeel", fg='white', bg='midnight blue', font=self.my_font2)
        self.label11.grid(row=4, column=0)

        # button2 = Button(master=hoofdframe, text='Waterkering sluiten', bd=1, command=button2)
        # button2.grid(row=5, column=0)

        # button3 = Button(master=hoofdframe, text='Waterkering openen', bd=1, command=button3, state='disabled')
        # button3.grid(row=5, column=1)

        self.label1 = Label(master=self.bovenframe, text="Status:", bg='midnight blue', fg='white', font=self.my_font2)
        self.label1.grid(row=0, column=0, sticky=W)

        self.label2 = Label(master=self.bovenframe, text="In werking", bg='midnight blue', fg='white', font=self.my_font2)
        self.label2.grid(row=0, column=1)

        self.label3 = Label(master=self.bovenframe, text="Kering:", bg='midnight blue', fg='white', font=self.my_font2)
        self.label3.grid(row=1, column=0, sticky=W)

        self.label4 = Label(master=self.bovenframe, text="OPEN", fg='green', bg='midnight blue', font=self.my_font2)
        self.label4.grid(row=1, column=1, sticky=W)

        self.label5 = Label(master=self.bovenframe, text="Waterpeil:", bg='midnight blue', fg='white', font=self.my_font2)
        self.label5.grid(row=2, column=0)

        self.label6 = Label(master=self.bovenframe, text="{} meter".format('3.5'), fg='white', bg='midnight blue', font=self.my_font2)
        self.label6.grid(row=2, column=1, sticky=W)

    def start(self):
        try:
            try:
                self.client_socket.connect((self.ip_address, self.port))
                self.connected_to_server = True
            except socket.error as e:
                if self.debug:
                    print("{} - Socket error {}".format(Gui.get_time(), e))
                sys.exit()
            finally:
                if self.debug:
                    print(
                    "{} - Successfully connect to IP:{}, PORT:{}".format(
                        Gui.get_time(), self.ip_address, self.port))

            start_new_thread(self.get_server_data, ())

            while True:
                self.debug = True
                self.socket_read()
        finally:
            self.stop_client()

    def stop_client(self):
        pass

    @staticmethod
    def get_time():
        """ Returns current time in format %d-%m-%Y %X """
        return datetime.datetime.now().strftime('%d-%m-%Y %X')

    def haal_gegevens_op(self):
        "Haalt gegevens op en schrijft dit weg in een csv bestand"
        with requests.Session() as s:   #Haalt gegevens op van de server
            download = s.get(self.csv_url)

            decoded_content = download.content.decode('utf-8')

            lezen = csv.reader(decoded_content.splitlines(), delimiter=';')
            lijst = list(lezen)


        with open(self.bestand_locatie, 'w', newline='') as myCSVFile:    #Schrijft gegevens weg in csv bestand
            schrijven = csv.writer(myCSVFile, delimiter=';')

            for lijn in lijst:
                schrijven.writerow(lijn)

    def toon_gegevens(self):
        'Zet de gegevens in een listbox met een bijbehorende kleur'
        with open(self.bestand_locatie, 'r') as myCSVFILE:  # Leest het geschreven csv bestand
            self.textVeld.delete(0, END)
            reader = csv.reader(myCSVFILE, delimiter=';')
            index = 2

            self.textVeld.insert(0, '{:19}{:15}{:21}{:18}{:4}'.format('Datum/tijd (MET)', '|Astronomisch', '|Gemeten waterstand',
                                                                  '|Verwachte opzet', '|Verwachting RWS'))
            self.textVeld.insert(1, '{:19}|{:14}|{:20}|{:17}|{:4}'.format('','','','',''))
            myCSVFILE.readline()

            for lijn in reader:  # Elke lijn met waardes komt in een tuple
                datum = lijn[0]
                astronomisch = lijn[1]
                waterstand = lijn[2]
                opzet = lijn[3]
                verw_RWS = lijn[4]

                self.textVeld.insert(index, '{:19}|{:14}|{:20}|{:17}|{:4}'.format(datum, astronomisch, waterstand, opzet, verw_RWS))
                if int(opzet) >= 30:
                    self.textVeld.itemconfig(index, {'fg': 'red'})
                elif int(opzet) >= 20 and int(opzet) < 30:
                    self.textVeld.itemconfig(index, {'fg': 'orange'})
                else:
                    self.textVeld.itemconfig(index, {'fg': 'green'})

                index += 1

    def parse_socket_data(self, data: str):
        """ Handles socket data accordingly """
        if data == "CLIENT_DATA":
            print(data)
        elif data == "UUID_REQ":
            self.socket_write(data_header="UUID", data=str(self.uuid))
        elif data == "REG_COMPLETE":
            self.registered = True

    def socket_write(self, data: str, data_header: str):
        """
            Writes a concatenation of the client UUID, data header and data to
            the connection socket of this program instance
        """
        message = str(self.uuid) + "," + data_header + "," + data
        if self.debug: print("{} - GUI send: {}".format(Gui.get_time(), message))

        try:
            self.client_socket.send(message.encode('ascii'))
        except ConnectionResetError or ConnectionAbortedError:
            if self.debug: print("{} - Connection has been terminated by the server.".format(self.get_time()))
            exit()
        self.client_socket.send(message.encode('ascii'))

    def socket_read(self):
        """
            Listens to the connection socket of this program instance
            and passes that data to the parse_socket_data() function
        """
        try:
            data = self.client_socket.recv(4096)
        except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
            if self.debug:
                print("{} - Connection has been terminated by the server.".format(Gui.get_time()))
            self.stop_client()
            sys.exit()
        data = data.decode('utf-8').strip().split(',')
        if self.debug:
            print("{} - Client received: {}".format(Gui.get_time(), data))
        if (data[0] == self.uuid) or (data[0] == "BROADCAST"):
            return self.parse_socket_data(data=data[1])

    def button1(self):
        #haal_gegevens_op()
        self.toon_gegevens()

    def button2(self):
        'Kering sluiten'
        self.label4['fg'] = 'red'
        self.label4['text'] = 'GESLOTEN'
        #button2['state'] = 'disabled'
        #button3['state'] = 'active'

    def button3(self):
        'Kering openen'
        self.label4['fg'] = 'green'
        self.label4['text'] = 'OPEN'
        #button3['state'] = 'disabled'
        #button2['state'] = 'active'

    def get_server_data(self):
        """ Sends a request to the server to get the latest client JSON data """
        while True:
            if self.connected_to_server:
                self.socket_write("", "GUI_UPDATE_REQ")
                time.sleep(2.5)

    def init_socket_read(self):
        """ socket_read() thread had to be called via another function to work """
        try:
            self.client_socket.connect((self.ip_address, self.port))
            self.connected_to_server = True
        except socket.error as e:
            if self.debug:
                print("{} - Socket error {}".format(Gui.get_time(), e))
            sys.exit()
        finally:
            if self.debug:
                print(
                    "{} - Successfully connect to IP:{}, PORT:{}".format(
                        Gui.get_time(), self.ip_address, self.port))
        while True:
            self.socket_read()


if __name__ == '__main__':
    try:
        gui = Gui("192.168.137.110", 5555, True)
        start_new_thread(gui.start, ())
        gui.mainloop()
    except Exception as e:
        print("There was an error initiating this node: {}".format(e))
