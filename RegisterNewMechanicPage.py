"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import tkinter as tk
import functools
from tkinter import *


class RegisterNewMechanicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f")
        self.backgroundContainer.configure(width=1000)
        self.backgroundContainer.configure(height=480)

        # Declaration of 'Back' Button
        self.notificationButton = Button(self.backgroundContainer)
        self.notificationButton.place(relx=0, rely=0,
                                      height=controller.buttonHeight,
                                      width=controller.buttonWidth)
        self.notificationButton.configure(text='Back')
        self.notificationButton.configure(
            command=functools.partial(controller.show_frame, "StartPage")
        )
        self.notificationButton.configure(
            background=controller.buttonBackgroundColor,
            foreground=controller.buttonForegroundColor,
            relief=controller.buttonRelief
        )
