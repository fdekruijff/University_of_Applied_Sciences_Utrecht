from tkinter import *
import math

root = Tk()

def clicked():
    cijfer = int(entry.get())
    kwadrant = cijfer * cijfer
    tekst = 'Het kwadrant van {} = {}'
    label['text'] = tekst.format(cijfer,kwadrant)

def wortel():
    cijfer = int(entry.get())
    wortel = math.sqrt(cijfer)
    tekst = 'De wortel van {} = {:.2f}'
    label['text'] = tekst.format(cijfer, wortel)



label = Label(master=root, text='Hello World', background='yellow', foreground='blue', font=('Helvetica', 16, 'bold italic'), width=25, height=3)
label.pack()

button = Button(master=root, text='Kwadrant', command=clicked)
button.pack(pady=10, fill=X, padx=25)

button = Button(master=root, text='Wortel', command=wortel)
button.pack(pady=10, fill=X, padx=25)

entry = Entry(master=root)
entry.pack(padx=10, pady=10)

root.mainloop()
