"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import operator
import tkinter as tk
import xml.etree.ElementTree as Et
import datetime
from math import *
from tkinter import *

import googlemaps
import requests

from CardMachine import CardMachine
from CardMachineOverviewPage import CardMachineOverviewPage
from GenerateMechanic import GenerateMechanic
from Mechanic import Mechanic
from MechanicOverviewPage import MechanicOverviewPage
from NotificationPage import NotificationPage
from RegisterNewMechanicPage import RegisterNewMechanicPage
from StartPage import StartPage
from Notification import Notification


class NSDefectOverview(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self)

        # Initialise variables
        self.frames = {}

        self.buttonWidth = 110,
        self.buttonHeight = 70
        self.buttonBackgroundColor = "#212b5c"
        self.buttonForegroundColor = "#ffffff"
        self.buttonRelief = FLAT

        self.width = 800
        self.height = 380

        self.cardMachineList = []
        self.mechanicList = []
        self.notificationList = [
            Notification(datetime.datetime.now(), "Just 1 random entry"),
            Notification(datetime.datetime.now(), "Just 2 random entry"),
            Notification(datetime.datetime.now(), "Just 3 random entry"),
            Notification(datetime.datetime.now(), "Just 4 random entry"),
            Notification(datetime.datetime.now(), "Just 5 random entry"),
            Notification(datetime.datetime.now(), "Just 6 random entry"),
            Notification(datetime.datetime.now(), "Just 7 random entry"),
            Notification(datetime.datetime.now(), "Just 8 random entry"),
            Notification(datetime.datetime.now(), "Just 9 random entry"),
            Notification(datetime.datetime.now(), "Just 1 random entry"),
            Notification(datetime.datetime.now(), "Just 2 random entry"),
            Notification(datetime.datetime.now(), "Just 3 random entry"),
            Notification(datetime.datetime.now(), "Just 4 random entry"),
            Notification(datetime.datetime.now(), "Just 5 random entry"),
            Notification(datetime.datetime.now(), "Just 6 random entry"),
            Notification(datetime.datetime.now(), "Just 7 random entry"),
            Notification(datetime.datetime.now(), "Just 8 random entry"),
            Notification(datetime.datetime.now(), "Just 9 random entry"),
            Notification(datetime.datetime.now(), "Just 1 random entry"),
            Notification(datetime.datetime.now(), "Just 2 random entry"),
            Notification(datetime.datetime.now(), "Just 3 random entry"),
            Notification(datetime.datetime.now(), "Just 4 random entry"),
            Notification(datetime.datetime.now(), "Just 5 random entry"),
            Notification(datetime.datetime.now(), "Just 6 random entry"),
            Notification(datetime.datetime.now(), "Just 7 random entry"),
            Notification(datetime.datetime.now(), "Just 8 random entry"),
            Notification(datetime.datetime.now(), "Just 9 random entry"),
            Notification(datetime.datetime.now(), "Just 1 random entry"),
            Notification(datetime.datetime.now(), "Just 2 random entry"),
            Notification(datetime.datetime.now(), "Just 3 random entry"),
            Notification(datetime.datetime.now(), "Just 4 random entry"),
            Notification(datetime.datetime.now(), "Just 5 random entry"),
            Notification(datetime.datetime.now(), "Just 6 random entry"),
            Notification(datetime.datetime.now(), "Just 7 random entry"),
            Notification(datetime.datetime.now(), "Just 8 random entry"),
            Notification(datetime.datetime.now(), "Just 9 random entry"),
            Notification(datetime.datetime.now(), "Just 10 random entry")
        ]

        self.ns_api_username = "floris.dekruijff@student.hu.nl"
        self.ns_api_password = "FK7CDKplQPsyOpBuPtkURW8incvUdT3T2ZSVoSkrTRdF7r5ARvCOyQ"
        self.google_maps_api = googlemaps.Client(key='AIzaSyB3sE6Ekts-GoPlZ8vJ8P8i0UL1rVFnnPI')

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
        # print(frame)

    def populate_card_machine_list(self):
        """ Populates the cardMachineList with generated Machines based on station """
        try:
            response = requests.get(url="http://webservices.ns.nl/ns-api-stations-v2",
                                    auth=(self.ns_api_username, self.ns_api_password)
                                    )
        except requests.exceptions.ConnectionError:
            exit("Failed to establish connection with NS API, please try again.")

        for element in Et.fromstring(response.text):
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
        """ Randomly generates meta data for a new mechanic. """
        for province in GenerateMechanic.regions:
            for amount in range(5):
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
        d = 6367 * c
        return d

    def get_closest_mechanic(self, card_machine: CardMachine):
        """
            This function loops through all the current mechanics and finds the one closest to the passed card machine
        """
        lowest = 0
        return_mechanic = None
        for mechanic in self.mechanicList:
            distance = self.haversine_formula(
                float(card_machine.latitude), float(card_machine.longitude),
                float(mechanic.latitude), float(mechanic.longitude)
            )
            if lowest == 0:
                lowest = distance
            elif distance < lowest:
                lowest = distance
                return_mechanic = mechanic
        return lowest, return_mechanic

    def get_distance_travel_time(self, latitude1, longitude1, latitude2, longitude2):
        """
            This function calculates and returns the distance and travel time based on two coordinates
            @:return: distance, travel time
        """
        result = self.google_maps_api.distance_matrix((latitude1, longitude1), (latitude2, longitude2))
        return (result['rows'][0]['elements'][0]['distance']['text'].split(' ')[0],
                result['rows'][0]['elements'][0]['duration']['text'].split(' ')[0])

    def new_popup(self, title: str, message: str, buttons: list, popup_width: int, popup_height: int,
                  background_color: str):
        """
            This function creates a pop-up based on the passed parameters. It also generates buttons based on the passed
            list.

            The button list should be in the following format:
            [
             {"text": "Lorem Ipsum", "command": "print *cannot contain ()*"},
             {"text": "Lorem Ipsum", "command": "print *cannot contain ()*"}
            ]
        """
        popup = tk.Tk()
        popup.wm_title(title)
        popup.geometry("{}x{}+{}+{}".format(
            popup_width,
            popup_height,
            int(self.winfo_x() + (self.width / 2 - popup_width / 2)),
            int(self.winfo_y() + (self.height / 2 - popup_height / 2))
        ))
        popup.configure(background=background_color)
        label = tk.Label(popup, text=message, background=background_color)
        label.pack(side="top", fill="x", pady=20, padx=20)

        if len(buttons) == 1:
            relative_x = 0.5
        else:
            relative_x = 1 / len(buttons) - 0.15

        rel_width = 80 / popup_width
        rel_height = 35 / popup_height
        for x in buttons:
            b = tk.Button(popup,
                          background=self.buttonBackgroundColor,
                          foreground=self.buttonForegroundColor,
                          relief=self.buttonRelief,
                          text=x['text'],
                          command=eval(x['command']))
            b.place(relwidth=rel_width, relheight=rel_height, relx=relative_x - (rel_width / 2), rely=0.45)
            relative_x += 0.3
        popup.mainloop()

    def dispatch_mechanic(self, card_machine: CardMachine, mechanic: Mechanic):
        """
            This function dispatches a mechanic to a card machine, and updates the logs for it.
            It will update the Notification center as well.
        """
        message = ""
        title = ""
        buttons = []
        if card_machine.defect == "Defect" and mechanic.availability == "Available":
            # Go directly to the create new event form.
            pass

        elif card_machine.defect == "Defect" and mechanic.availability == "Occupied":
            # TODO: Maybe find the next closest available mechanic.
            title = "Unfortunately"
            message = "Unfortunately {} is {}, but {} is {}".format(
                card_machine.station_name, card_machine.defect, mechanic.name, mechanic.availability.lower()
            )
            buttons = [{"text": "Ok", "command": "popup.destroy"}]

        elif card_machine.defect == "Operational" and mechanic.availability == "Occupied":
            # TODO: Maybe find the next closest available mechanic.
            title = "Are you sure?"
            message = "{} is {}, but {} is {}".format(
                card_machine.station_name, card_machine.defect, mechanic.name, mechanic.availability.lower()
            )
            buttons = [{"text": "Yes, I'm sure", "command": "0", "mechanic": mechanic, "card_machine": card_machine},
                       {"text": "Cancel", "command": "popup.destroy"}]

        elif card_machine.defect == "Operational" and mechanic.availability == "Available":
            title = "Are you sure?"
            message = "{} is {} and {} is {}".format(
                card_machine.station_name, card_machine.defect, mechanic.name, mechanic.availability.lower()
            )
            buttons = [{"text": "Yes, I'm sure", "command": "0", "mechanic": mechanic, "card_machine": card_machine},
                       {"text": "Cancel", "command": "popup.destroy"}]

        self.new_popup(title, message, buttons, 450, 150, "#fcc63f")
