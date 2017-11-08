"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import tkinter as tk
import functools
from tkinter import *


class NotificationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

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
        self.searchEntry.insert(0, "Search Notification")
        self.searchEntry.bind('<FocusIn>', self.on_entry_click)
        self.searchEntry.bind("<Key>", self.search_notification)

        self.notificationListBox = Listbox(self.backgroundContainer)
        self.notificationListBox.place(relx=0.020, rely=0.15, relwidth=0.96, relheight=0.80)
        self.notificationListBox.configure(background="#ebedeb")
        self.notificationListBox.configure(foreground=self.controller.buttonBackgroundColor)
        self.notificationListBox.configure(relief=self.controller.buttonRelief)
        self.notificationListBox.configure(highlightbackground="#fcc63f")
        self.notificationListBox.configure(activestyle='none')
        self.notificationListBox.configure(highlightcolor="#fcc63f")
        self.notificationListBox.configure(selectbackground="#ebedeb")
        self.notificationListBox.configure(selectforeground="#212b5c")
        self.notificationListBox.configure(width=500)
        self.notificationListBox.configure(height=100)

        self.scrollbar = Scrollbar(self.notificationListBox)
        self.notificationListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.notificationListBox.yview)

        self.update_notification_list()

    def on_entry_click(self, x):
        self.controller.log("NotificationPage.on_entry_click()")
        if self.searchEntry.get() == 'Search Notification':
            self.searchEntry.delete(0, END)
            self.searchEntry.insert(0, '')
            self.searchEntry.config(fg='black')

    def update_notification_list(self):
        self.controller.log("NotificationPage.update_notification_list()")
        self.notificationListBox.delete(0,  END)
        for notification in self.controller.notificationList:
            entry = "{time}" \
                    "                       " \
                    "{message}".format(time=notification.time, message= notification.message)
            self.notificationListBox.insert(0, entry)

    def search_notification(self, key):
        self.controller.log("NotificationPage.search_notification(key={)".format(key))
        if self.searchEntry.get() == "" or not key:
            self.notificationListBox.delete(0, END)
            for notification in self.controller.notificationList:
                entry = "{time}" \
                        "                       " \
                        "{message}".format(time=notification.time, message=notification.message)
                self.notificationListBox.insert(END, entry)
        else:
            self.notificationListBox.delete(0, END)
            for notification in self.controller.notificationList:
                entry = "{time}" \
                        "                       " \
                        "{message}".format(time=notification.time, message=notification.message)
                if self.searchEntry.get().lower().strip() in entry.lower():
                    self.notificationListBox.insert(END, entry)
