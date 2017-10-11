"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import functools
import math
import tkinter as tk
from tkinter import *


class CardMachineOverviewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.searchString = []
        self.informationLabels = ["Card Machine Station: ", "Longitude: ", "Latitude: ", "In service: ", "Name: ",
                                  "Direct Distance: ", ""]
        self.informationHeaders = ["General Card Machine Information", "Closest Mechanic"]

        # Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f")
        self.backgroundContainer.configure(width=1000)
        self.backgroundContainer.configure(height=480)

        # Declaration of 'Back' Button
        self.notificationButton = Button(self.backgroundContainer)
        self.notificationButton.place(relx=0, rely=0, relheight=0.10, relwidth=0.25)
        self.notificationButton.configure(text='Back')
        self.notificationButton.configure(
            command=functools.partial(self.controller.show_frame, "StartPage")
        )
        self.notificationButton.configure(
            background=self.controller.buttonBackgroundColor,
            foreground=self.controller.buttonForegroundColor,
            relief=self.controller.buttonRelief
        )

        self.searchEntry = Entry(self.backgroundContainer)
        self.searchEntry.place(relx=0.25, rely=0.0, relheight=0.10, relwidth=0.75)
        self.searchEntry.configure(background="white")
        self.searchEntry.configure(foreground="grey")
        self.searchEntry.configure(insertbackground="black")
        self.searchEntry.configure(justify='center')
        self.searchEntry.insert(0, "Search Station")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_station)

        self.stationListBox = Listbox(self.backgroundContainer)
        self.stationListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
        self.stationListBox.configure(background="#ebedeb")
        self.stationListBox.configure(foreground=self.controller.buttonBackgroundColor)
        self.stationListBox.configure(relief=self.controller.buttonRelief)
        self.stationListBox.configure(highlightbackground="#fcc63f")
        self.stationListBox.configure(highlightcolor="#fcc63f")
        self.stationListBox.configure(width=500)
        self.stationListBox.configure(height=100)
        self.stationListBox.bind("<Double-Button-1>", self.get_machine_specifics)

        self.scrollbar = Scrollbar(self.stationListBox)
        self.stationListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.stationListBox.yview)

        self.informationContainer = Frame(self.backgroundContainer)
        self.tempLabel = None

        self.search_station(None)

    def search_station(self, key):
        if self.searchEntry.get() == "" or not key:
            for station in self.controller.cardMachineList:
                self.stationListBox.insert(END, station.station_name)
        else:
            self.stationListBox.delete(0, END)
            for station in self.controller.cardMachineList:
                if self.searchEntry.get().lower().strip() in station.station_name.lower():
                    self.stationListBox.insert(END, station.station_name)

    def on_entry_click(self, x):
        if self.searchEntry.get() == 'Search Station':
            self.searchEntry.delete(0, END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')

    def calculate_distance_time_popup(self, card_machine, mechanic_info):
        travel_advice = self.controller.get_distance_travel_time(
            card_machine.latitude, card_machine.longitude,
            mechanic_info[1].latitude, mechanic_info[1].longitude
        )

        self.controller.new_popup(
            "Travel information",
            "Traveling to {} by car will be {} kilometer over {} minutes.".format(
                card_machine.station_name, travel_advice[0], travel_advice[1]
            ),
            [{"text": "  Done  ", "command": "self.popup.destroy"}],
            450, 100, "#fcc63f"
        )

    def update_machine_specifics_labels(self, card_machine_info, card_machine, mechanic_info):
        rely = 0
        for label in self.informationHeaders:
            self.tempLabel = Label(self.informationContainer)
            self.tempLabel.place(relx=0, rely=rely, relwidth=1, relheight=0.15)
            self.tempLabel.configure(text=label)
            self.tempLabel.configure(background="#ebedeb")
            self.tempLabel.configure(font="Helvetica 12 bold")
            rely += 0.575

        rely = 0.15
        for label in range(len(self.informationLabels)):
            if label == 4:
                rely += 0.22

            if card_machine_info[label] != "":
                self.tempLabel = Label(self.informationContainer)
                self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
                self.tempLabel.configure(background="#ebedeb")
                self.tempLabel.configure(text=self.informationLabels[label])
                self.tempLabel.configure(anchor='w')

                self.tempLabel = Label(self.informationContainer)
                self.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
                self.tempLabel.configure(anchor='w')
                self.tempLabel.configure(background="#ebedeb")
                self.tempLabel.configure(text=card_machine_info[label])

            else:
                self.tempLabel = Button(self.informationContainer)
                self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
                self.tempLabel.configure(anchor='w')
                self.tempLabel.configure(
                    command=functools.partial(self.controller.dispatch_mechanic, card_machine, mechanic_info[1])
                )
                self.tempLabel.configure(
                    background=self.controller.buttonBackgroundColor,
                    foreground=self.controller.buttonForegroundColor,
                    relief=self.controller.buttonRelief
                )
                self.tempLabel.configure(text=" Dispatch Mechanic ")

                self.tempLabel = Button(self.informationContainer)
                self.tempLabel.place(relx=0.5, rely=rely, relwidth=0.425)
                self.tempLabel.configure(anchor='w')
                self.tempLabel.configure(
                    command=functools.partial(self.calculate_distance_time_popup, card_machine, mechanic_info)
                )
                self.tempLabel.configure(
                    background=self.controller.buttonBackgroundColor,
                    foreground=self.controller.buttonForegroundColor,
                    relief=self.controller.buttonRelief
                )
                self.tempLabel.configure(text=" Calculate Travel Time ")
            rely += 0.085

    def get_machine_specifics(self, x):
        station_input = x.widget.get(x.widget.curselection()[0])
        card_machine = None
        card_machine_info = []

        for machine in self.controller.cardMachineList:
            if machine.station_name.lower() == station_input.lower():
                card_machine = machine

        mechanic_info = self.controller.get_closest_mechanic(card_machine)

        card_machine_info.append(card_machine.station_name)
        card_machine_info.append(card_machine.longitude)
        card_machine_info.append(card_machine.latitude)
        card_machine_info.append(card_machine.defect)
        card_machine_info.append(mechanic_info[1].name)
        card_machine_info.append("{} km".format(math.floor(mechanic_info[0])))
        card_machine_info.append("")

        self.informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
        self.informationContainer.configure(background="#ebedeb")
        self.update_machine_specifics_labels(card_machine_info, card_machine, mechanic_info)
