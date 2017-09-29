"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
    Responsibility: Floris de Kruijff
"""

import functools
import tkinter as tk
from tkinter import *


class CardMachineOverviewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.searchString = []

        # Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f")
        self.backgroundContainer.configure(width=1000)
        self.backgroundContainer.configure(height=480)

        # Declaration of 'Back' Button
        self.notificationButton = Button(self.backgroundContainer)
        self.notificationButton.place(relx=0, rely=0,
                                      relheight=0.10,
                                      relwidth=0.25)
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
        self.searchEntry.configure(disabledforeground="#a3a3a3")
        self.searchEntry.configure(foreground="grey")
        self.searchEntry.configure(insertbackground="black")
        self.searchEntry.configure(justify='center')
        self.searchEntry.insert(0, "Search Station")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_station)

        self.StationListBox = Listbox(self.backgroundContainer)
        self.StationListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
        self.StationListBox.configure(background="#ffffff")
        self.StationListBox.configure(foreground=self.controller.buttonBackgroundColor)
        self.StationListBox.configure(relief=self.controller.buttonRelief)
        self.StationListBox.configure(highlightbackground="#fcc63f")
        self.StationListBox.configure(highlightcolor="#fcc63f")
        self.StationListBox.configure(width=500)
        self.StationListBox.configure(height=100)

        scrollbar = Scrollbar(self.StationListBox)
        scrollbar.pack(side=RIGHT, fill=Y)

        for station in self.controller.cardMachineList:
            self.StationListBox.insert(END, station.station_name)

        self.StationListBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.StationListBox.yview)

    def search_station(self, key):
        if (key.keycode == 8) and (len(self.searchString) != 0):
            # Remove last element from list
            del self.searchString[-1]
        elif 65 <= key.keycode <= 90:
            # These are all the letters
            self.searchString.append(key.keysym)
        elif key.keycode in [32, 222, 189]:
            self.searchString.append(key.char)

        string = ''.join(self.searchString)

        if string == "":
            self.StationListBox.delete(0, END)
            for station in self.controller.cardMachineList:
                self.StationListBox.insert(END, station.station_name)
        else:
            self.StationListBox.delete(0, END)
            for station in self.controller.cardMachineList:
                if string.lower().strip() in station.station_name.lower():

                    self.StationListBox.insert(END, station.station_name)

    def on_entry_click(self, x):
        if self.searchEntry.get() == 'Search Station':
            self.searchEntry.delete(0, "end")
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')
