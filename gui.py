#GUI Alarmsysteem
from functools import *
from tkinter import *
from playsound import *
from math import *

root = Tk()
serverbool = True
staataan = True

root.geometry("{}x{}+400+150".format(800,500))
root.title("Alarmsysteem")
root.resizable(0, 0)
root.configure(background="#ebedeb")


def buttonClick():
    global staataan
    staataan = False if staataan else True
    print(staataan)
    if button.bg == "green":
        root.button.configure(bg = "red")
    else:
        root.button.configure(bg = "green")

root.informationContainer = Frame()
root.mechanicListBox = Listbox()
root.mechanicListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
root.mechanicListBox.configure(background="white")
root.mechanicListBox.configure(foreground="black")
root.mechanicListBox.configure(relief=RAISED)
root.mechanicListBox.configure(highlightbackground="black")
root.mechanicListBox.configure(highlightcolor="black")
root.mechanicListBox.configure(width=500)
root.mechanicListBox.configure(height=100)
root.mechanicListBox.bind("<Double-Button-1>")

root.informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
root.informationContainer.configure(background="white")
root.informationContainer.configure(highlightbackground="black")
root.informationContainer.configure(highlightcolor="black")


button = Button(root, text = "      Alarm Set     " if staataan else "      Alarm Disabled      ", bg = "green" if
                staataan else "red", command = buttonClick)
button.grid(row=0,column=0)
button.config(font=("Courier", 11))

#button.grid(row=1,column=0,pady=50)

label = Label(root, text = "Status Alarm:\n" + ("HET ALARM GAAT AF" if serverbool else "ER GAAT GEEN ALARM AF"))
label.grid(row=0,column=1,padx=300)
label.config(font=("Courier", 11))

mainloop()
