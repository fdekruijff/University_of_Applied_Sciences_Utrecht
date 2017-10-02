"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import tkinter as tk
from tkinter import Frame
from tkinter import Button
from tkinter import Label
import functools


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.backgroundImage = tk.PhotoImage(file="images/ns_logo_1_50.png")

        # Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f")
        self.backgroundContainer.configure(width=1000)
        self.backgroundContainer.configure(height=480)
        self.button_information = [
            ["Notifications", "NotificationPage", 0.0],
            ["Overview\nCard Machines", "CardMachineOverviewPage", 0.2],
            ["Overview\nMechanics", "MechanicOverviewPage", 0.6625],
            ["Register\nNew Mechanic", "RegisterNewMechanicPage", 0.8625]
        ]

        # Declaration of background Label
        self.backgroundImageContainer = Label(self.backgroundContainer, image=self.backgroundImage)
        self.backgroundImageContainer.place(
            relx=((controller.width / 2) - (self.backgroundImage.width() / 2)) * 0.5 / (controller.width / 2),
            rely=((controller.height / 2) - (self.backgroundImage.height() / 2)) * 0.5 / (controller.height / 2),
            height=self.backgroundImage.height(), width=self.backgroundImage.width())

        # Declaring buttons based on button_information list
        for button in self.button_information:
            self.notificationButton = Button(self.backgroundContainer)
            self.notificationButton.place(relx=button[2], rely=0,
                                          height=controller.buttonHeight,
                                          width=controller.buttonWidth)
            self.notificationButton.configure(text=button[0])
            self.notificationButton.configure(
                command=functools.partial(controller.show_frame, button[1])
            )
            self.notificationButton.configure(
                background=controller.buttonBackgroundColor,
                foreground=controller.buttonForegroundColor,
                relief=controller.buttonRelief
            )
