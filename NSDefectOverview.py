"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import requests

import tkinter as tk
import xml.etree.ElementTree as Et

from math import *
from tkinter import *
from CardMachineOverviewPage import CardMachineOverviewPage
from MechanicOverviewPage import MechanicOverviewPage
from NotificationPage import NotificationPage
from RegisterNewMechanicPage import RegisterNewMechanicPage
from StartPage import StartPage
from CardMachine import CardMachine
from GenerateMechanic import GenerateMechanic
import operator


class NSDefectOverview(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self)

        # Initialise variables
        self.frames = {}

        self.buttonWidth = 110
        self.buttonHeight = 70
        self.buttonBackgroundColor = "#212b5c"
        self.buttonForegroundColor = "#ffffff"
        self.buttonRelief = FLAT

        self.width = 800
        self.height = 380

        self.cardMachineList = []
        self.mechanicList = []

        self.ns_api_username = "floris.dekruijff@student.hu.nl"
        self.ns_api_password = "FK7CDKplQPsyOpBuPtkURW8incvUdT3T2ZSVoSkrTRdF7r5ARvCOyQ"

        self.geometry("{}x{}+400+150".format(self.width, self.height))
        self.title("NS Defect Overview")
        self.resizable(0, 0)

        # Initialise data
        self.populate_card_machine_list()
        self.populate_mechanic_list()

        # Initialise TkInter container settings.
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for page in (StartPage,
                     MechanicOverviewPage,
                     RegisterNewMechanicPage,
                     CardMachineOverviewPage,
                     NotificationPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.frames[StartPage] = StartPage(container, self)
        StartPage(container, self).grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def populate_card_machine_list(self):
        """ Populates the cardMachineList with generated Machines based on station """
        response = requests.get(url="http://webservices.ns.nl/ns-api-stations-v2",
                                auth=(self.ns_api_username, self.ns_api_password)
                                )

        root = Et.fromstring(response.text)

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

            # We only want stations based in the Netherlands
            if is_in_netherlands:
                self.cardMachineList.append(CardMachine(station_name, longitude, latitude))

    def populate_mechanic_list(self):
        """ Generates a number of people per province """
        for province in GenerateMechanic.regions:
            for amount in range(15):
                self.mechanicList.append(GenerateMechanic.generate_mechanic(province))
        self.mechanicList.sort(key=operator.attrgetter('name'))

    def haversine_formula(self, latitude1, longitude1, latitude2, longitude2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
        # haversine formula
        delta_longitude = longitude2 - longitude1
        delta_latitude = latitude2 - latitude1
        a = sin(delta_latitude / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(delta_longitude / 2) ** 2
        c = 2 * asin(sqrt(a))
        return 6367 * c

    def get_closest_mechanic(self, card_machine: CardMachine):
        lowest = 0
        return_mechanic = None
        latitude1 = card_machine.latitude
        longitude1 = card_machine.longitude
        for mechanic in self.mechanicList:
            distance = self.haversine_formula(float(latitude1), float(longitude1), float(mechanic.latitude), float(mechanic.longitude))
            if lowest == 0:
                lowest = distance
            elif distance < lowest:
                lowest = distance
                return_mechanic = mechanic
        return lowest, return_mechanic
