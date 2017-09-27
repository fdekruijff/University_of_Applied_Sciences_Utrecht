"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
    Responsibility: Floris de Kruijff
"""

import tkinter as tk
import requests
import xml.etree.ElementTree as ET

from CardMachineOverviewPage import CardMachineOverviewPage
from MechanicOverviewPage import MechanicOverviewPage
from NotificationPage import NotificationPage
from RegisterNewMechanicPage import RegisterNewMechanicPage
from StartPage import StartPage
from CardMachine import CardMachine


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self)

        # Initialise variables
        self.width = 800
        self.height = 380
        self.cardMachineList = []

        # Initialise TkInter container settings.
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for page in (StartPage,
                     MechanicOverviewPage,
                     RegisterNewMechanicPage,
                     CardMachineOverviewPage,
                     NotificationPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = StartPage(container, self)

        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

        self.geometry("{}x{}+400+150".format(self.width, self.height))
        self.title("NS Defect Overview")
        self.resizable(0, 0)

        self.populate_card_machine_list(self.cardMachineList)

        print(len(self.cardMachineList))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def populate_card_machine_list(self, card_machine_list: list):
        """ Populates the cardMachineList with generated Machines based on station """

        response = requests.get(url="http://webservices.ns.nl/ns-api-stations-v2",
                                auth=(
                                    'niek.geijtenbeek@gmail.com',
                                    'VyYLUiVS6cYkg51tWeifVUpvc_q79yytICH548rmSj31Y8Bk5QWjZg'))

        root = ET.fromstring(response.text)

        for element in root:
            is_in_netherlands = False
            station_name = ""
            latitude = ""
            longitude = ""
            for meta in element:
                if meta.tag == "Namen":
                    for name in meta:
                        if name.tag == "Lang":
                            station_name = name.text

                if meta.text == "NL":
                    is_in_netherlands = True

                if meta.tag == "Lat":
                    latitude = meta.text
                if meta.tag == "Lon":
                    longitude = meta.text

            if is_in_netherlands:
                card_machine_list.append(CardMachine(station_name, longitude, latitude))


if __name__ == '__main__':
    program = Main()
    program.mainloop()
