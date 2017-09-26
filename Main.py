"""
    Title: 
    Author: Floris de Kruijff
    Date created: 26-Sep-17
"""

import tkinter as tk
from StartPagina import StartPagina
from MoneurOverzicht import MonteurOverzicht


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self)

        self.width = 800
        self.height = 380

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPagina, MonteurOverzicht):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = StartPagina(container, self)

        self.frames[StartPagina] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPagina)

        self.geometry("{}x{}+400+150".format(self.width, self.height))
        self.title("NS Defectoverzicht")
        self.resizable(0, 0)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


if __name__ == '__main__':
    program = Main()
    program.mainloop()
