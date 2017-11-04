"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
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
            ["Notifications", "NotificationPage"],
            ["Overview\nCard Machines", "CardMachineOverviewPage"],
            ["Overview\nMechanics", "MechanicOverviewPage"]
        ]

        self.informationLabel = Label(self.backgroundContainer)
        self.informationLabel.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        self.informationLabel.configure(text="Floris de Kruijff"
                                             "     -     "
                                             "Bryan Campagne"
                                             "     -     "
                                             "Rik van Velzen"
                                             "\n\n"
                                             "TICT-V1PROG-15")
        self.informationLabel.configure(
                background=controller.buttonBackgroundColor,
                foreground=controller.buttonForegroundColor,
                relief=controller.buttonRelief
            )

        # Declaration of background Label
        self.backgroundImageContainer = Label(self.backgroundContainer, image=self.backgroundImage)
        self.backgroundImageContainer.place(
            relx=((controller.width / 2) - (self.backgroundImage.width() / 2)) * 0.5 / (controller.width / 2),
            rely=((controller.height / 2) - (self.backgroundImage.height() / 2)) * 0.5 / (controller.height / 2),
            height=self.backgroundImage.height(), width=self.backgroundImage.width())

        # Declaring buttons based on button_information list
        rel_x = 0.0
        for button in self.button_information:
            self.notificationButton = Button(self.backgroundContainer)
            self.notificationButton.place(relx=rel_x, rely=0,
                                          relheight=0.10,
                                          relwidth=0.25)
            self.notificationButton.configure(text=button[0])
            self.notificationButton.configure(
                command=functools.partial(controller.show_frame, button[1])
            )
            self.notificationButton.configure(
                background=controller.buttonBackgroundColor,
                foreground=controller.buttonForegroundColor,
                relief=controller.buttonRelief
            )

            rel_x += 0.375
