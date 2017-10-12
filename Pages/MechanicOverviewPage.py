"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import functools
import tkinter as tk
from tkinter import *


class MechanicOverviewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.searchString = []
        self.informationLabels = ["Name: ", "Region: ", "Age: ", "Availability: ","Shift: "]
        self.informationHeaders = ["General Information", "Actions"]

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
        self.searchEntry.insert(0, "Search Mechanic")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_mechanic)

        self.mechanicListBox = Listbox(self.backgroundContainer)
        self.mechanicListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
        self.mechanicListBox.configure(background="#ebedeb")
        self.mechanicListBox.configure(foreground=self.controller.buttonBackgroundColor)
        self.mechanicListBox.configure(relief=self.controller.buttonRelief)
        self.mechanicListBox.configure(highlightbackground="#fcc63f")
        self.mechanicListBox.configure(highlightcolor="#fcc63f")
        self.mechanicListBox.configure(width=500)
        self.mechanicListBox.configure(height=100)
        self.mechanicListBox.bind("<Double-Button-1>", self.get_mechanic_specifics)

        self.scrollbar = Scrollbar(self.mechanicListBox)
        self.mechanicListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.mechanicListBox.yview)

        self.informationContainer = Frame(self.backgroundContainer)
        self.tempLabel = None
        self.search_mechanic(None)

    def search_mechanic(self, key):
        if self.searchEntry.get() == "" or not key:
            for mechanic in self.controller.mechanicList:
                self.mechanicListBox.insert(END, mechanic.name)
        else:
            self.mechanicListBox.delete(0, END)
            for mechanic in self.controller.mechanicList:
                if self.searchEntry.get().lower().strip() in mechanic.name.lower():
                    self.mechanicListBox.insert(END, mechanic.name)
                elif self.searchEntry.get().lower().strip() in mechanic.region.lower():
                    self.mechanicListBox.insert(END, mechanic.name)

    def on_entry_click(self, x):
        if self.searchEntry.get() == "Search Mechanic":
            self.searchEntry.delete(0, END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')

    def get_mechanic_specifics(self, x):
        mechanic_input = x.widget.get(x.widget.curselection()[0])
        mechanic = None
        mechanic_info = []

        for found_mechanic in self.controller.mechanicList:
            if found_mechanic.name.lower() == mechanic_input.lower():
                mechanic = found_mechanic

        mechanic_info.append(mechanic.name)
        mechanic_info.append(mechanic.region.title())
        mechanic_info.append(mechanic.age)
        mechanic_info.append(mechanic.availability)
        mechanic_info.append(mechanic.shift)

        self.informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
        self.informationContainer.configure(background="#ebedeb")

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
            self.tempLabel = Label(self.informationContainer)
            self.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
            self.tempLabel.configure(background="#ebedeb")
            self.tempLabel.configure(text=self.informationLabels[label])
            self.tempLabel.configure(anchor='w')

            self.tempLabel = Label(self.informationContainer)
            self.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
            self.tempLabel.configure(anchor='w')
            self.tempLabel.configure(background="#ebedeb")
            self.tempLabel.configure(text=mechanic_info[label])
            rely += 0.085
