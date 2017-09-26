import tkinter as tk
from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import FLAT


class StartPagina(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.backgroundImage = tk.PhotoImage(file="lib/images/ns_logo_1_50.png")
        self.buttonWidth = 110
        self.buttonHeight = 70

        # Background Frame
        self.backgroundContainer = Frame(self)
        self.backgroundContainer.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.backgroundContainer.configure(background="#fcc63f")
        self.backgroundContainer.configure(width=1000)
        self.backgroundContainer.configure(height=480)

        self.backgroundImageContainer = Label(self.backgroundContainer, image=self.backgroundImage)
        self.backgroundImageContainer.place(
            relx=((controller.get_width() / 2) - (self.backgroundImage.width() / 2)) * 0.5 / (controller.get_width() / 2),
            rely=((controller.get_height() / 2) - (self.backgroundImage.height() / 2)) * 0.5 / (controller.get_height() / 2),
            height=self.backgroundImage.height(), width=self.backgroundImage.width())

        self.Button1 = Button(self.backgroundContainer)
        self.Button1.place(relx=0, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.Button1.configure(background="#212b5c")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(relief=FLAT)
        self.Button1.configure(text='Meldingen')

        self.Button2 = Button(self.backgroundContainer)
        self.Button2.place(relx=0.2, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.Button2.configure(background="#212b5c")
        self.Button2.configure(foreground="#ffffff")
        self.Button2.configure(relief=FLAT)
        self.Button2.configure(text='Overzicht\nKaartautomaten')

        self.Button3 = Button(self.backgroundContainer)
        self.Button3.place(relx=0.6625, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.Button3.configure(background="#212b5c")
        self.Button3.configure(foreground="#ffffff")
        self.Button3.configure(relief=FLAT)
        self.Button3.configure(text='Overzicht\nMonteurs')

        self.Button4 = Button(self.backgroundContainer)
        self.Button4.place(relx=0.8625, rely=0, height=self.buttonHeight, width=self.buttonWidth)
        self.Button4.configure(background="#212b5c")
        self.Button4.configure(foreground="#ffffff")
        self.Button4.configure(relief=FLAT)
        self.Button4.configure(text='Registreer\nNieuwe Monteur')