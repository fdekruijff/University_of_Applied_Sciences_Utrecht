"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
    Responsibility: Floris de Kruijff
"""

import tkinter as tk
from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import FLAT


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.backgroundImage = tk.PhotoImage(file="images/ns_logo_1_50.png")
        self.buttonWidth = 110
        self.buttonHeight = 70
        self.buttonBackgroundColor = "#212b5c"
        self.buttonForegroundColor = "#ffffff"
        self.buttonRelief = FLAT

        # Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f")
        self.backgroundContainer.configure(width=1000)
        self.backgroundContainer.configure(height=480)

        # Declaration of background Label
        self.backgroundImageContainer = Label(self.backgroundContainer, image=self.backgroundImage)
        self.backgroundImageContainer.place(
            relx=((controller.get_width() / 2) - (self.backgroundImage.width() / 2)) * 0.5 / (controller.get_width() / 2),
            rely=((controller.get_height() / 2) - (self.backgroundImage.height() / 2)) * 0.5 / (controller.get_height() / 2),
            height=self.backgroundImage.height(), width=self.backgroundImage.width())

        # Declaration of 'Notifications' Button
        self.notificationButton = Button(self.backgroundContainer)
        self.notificationButton.place(relx=0, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.notificationButton.configure(text='Notifications')
        self.notificationButton.configure(
            command=lambda: controller.show_frame("NotificationPage")
        )
        self.notificationButton.configure(
            background=self.buttonBackgroundColor, foreground=self.buttonForegroundColor, relief=self.buttonRelief
        )

        # Declaration of 'Overview Card Machines' Button
        self.cardMachineOverviewButton = Button(self.backgroundContainer)
        self.cardMachineOverviewButton.place(relx=0.2, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.cardMachineOverviewButton.configure(text='Overview\nCard Machines')
        self.cardMachineOverviewButton.configure(
            command=lambda: controller.show_frame("CardMachineOverviewPage")
        )
        self.cardMachineOverviewButton.configure(
            background=self.buttonBackgroundColor, foreground=self.buttonForegroundColor, relief=self.buttonRelief
        )

        # Declaration of 'Overview Mechanics' Button
        self.mechanicOverviewButton = Button(self.backgroundContainer)
        self.mechanicOverviewButton.place(relx=0.6625, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.mechanicOverviewButton.configure(text='Overview\nMechanics')
        self.mechanicOverviewButton.configure(
            command=lambda: controller.show_frame("MechanicOverviewPage")
        )
        self.mechanicOverviewButton.configure(
            background=self.buttonBackgroundColor, foreground=self.buttonForegroundColor, relief=self.buttonRelief
        )

        # Declaration of 'Register New Mechanic' Button
        self.registerNewMechanicButton = Button(self.backgroundContainer)
        self.registerNewMechanicButton.place(relx=0.8625, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.registerNewMechanicButton.configure(text='Register\nNew Mechanic')
        self.registerNewMechanicButton.configure(
            command=lambda: controller.show_frame("RegisterNewMechanicPage")
        )
        self.registerNewMechanicButton.configure(
            background=self.buttonBackgroundColor, foreground=self.buttonForegroundColor, relief=self.buttonRelief
        )
