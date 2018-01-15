from tkinter import *
from winsound import *

root = Tk()
exorcist = PhotoImage(file='exorcist.gif')

def clicked():
    label['image'] = exorcist
    label['width'] = 1000
    label['height'] = 500
    label2['text'] = 'Boe'
    PlaySound('scream.wav', SND_FILENAME)

label2 = Label(master=root, text='', width=25, font=('Arial Black', 50))
label2.pack()

label = Label(master=root, text='', width=25, height=3)
label.pack(fill='both')



button = Button(master=root, text='DRUK HIER NIET!', command=clicked)
button.pack(pady=10, fill=X, padx=25)

root.mainloop()