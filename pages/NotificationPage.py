"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import tkinter as tk
import functools
from tkinter import *


class NotificationPage(tk.Frame):
    """
        This TkInter object holds all information for all Notification objects,
        this is just an overview list that can be searched.
    """

    def __init__(self, parent, controller):
        """ Object constructor """
        tk.Frame.__init__(self, parent)

        # Initialise variables
        self.controller = controller

        # Declaration of Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f", width=1000, height=480)

        # Declaration of 'Back' Button
        self.notificationButton = Button(self.backgroundContainer)
        self.notificationButton.place(relx=0, rely=0, relheight=0.10, relwidth=0.25)
        self.notificationButton.configure(
            text='Back',
            command=functools.partial(self.controller.show_frame, "StartPage"),
            background=self.controller.buttonBackgroundColor,
            foreground=self.controller.buttonForegroundColor,
            relief=self.controller.buttonRelief
        )

        self.searchEntry = Entry(self.backgroundContainer)
        self.searchEntry.place(relx=0.25, rely=0.0, relheight=0.10, relwidth=0.75)
        self.searchEntry.configure(background="white", foreground="grey", insertbackground="black", justify="center")
        self.searchEntry.insert(0, "Search Notification")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_notification)

        self.notificationListBox = Listbox(self.backgroundContainer)
        self.notificationListBox.place(relx=0.020, rely=0.15, relwidth=0.96, relheight=0.80)
        self.notificationListBox.configure(
            background="#ebedeb",
            foreground=self.controller.buttonBackgroundColor,
            relief=self.controller.buttonRelief,
            highlightbackground="#fcc63f",
            highlightcolor="#fcc63f",
            width=500, height=100
        )

        self.scrollbar = Scrollbar(self.notificationListBox)
        self.notificationListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.notificationListBox.yview)

        self.update_notification_list()

    def on_entry_click(self, x):
        """ If searchEntry is clicked and has default text in it, it is removed. """
        self.controller.log("NotificationPage.on_entry_click()")
        if self.searchEntry.get() == 'Search Notification':
            self.searchEntry.delete(0, END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')

    def update_notification_list(self):
        """ Updates the listBox with all elements from controller.notifcationList. """
        self.controller.log("NotificationPage.update_notification_list()")
        self.notificationListBox.delete(0,  END)
        for notification in self.controller.notificationList:
            entry = "{time}                       {message}"\
                .format(time=notification.time, message=notification.message)
            self.notificationListBox.insert(0, entry)

    def search_notification(self, key):
        """
            Function takes searchEntry input and searches corresponding Notification with it.
            Can be based on entry only.
        """
        self.controller.log("NotificationPage.search_notification(key={)".format(key))
        if self.searchEntry.get() == "" or not key:
            self.notificationListBox.delete(0, END)
            for notification in self.controller.notificationList:
                entry = "{time}                       {message}" \
                    .format(time=notification.time, message=notification.message)
                self.notificationListBox.insert(END, entry)
        else:
            self.notificationListBox.delete(0, END)
            for notification in self.controller.notificationList:
                entry = "{time}                       {message}" \
                    .format(time=notification.time, message=notification.message)
                # Match to entry
                if self.searchEntry.get().lower().strip() in entry.lower():
                    self.notificationListBox.insert(END, entry)
