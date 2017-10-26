#GUI Alarmsysteem
from functools import *
from tkinter import *
from ClientNode import ClientNode
from playsound import *
from math import *

root = Tk()
serverbool = True
staataan = True

root.geometry("{}x{}+400+150".format(800,500))
root.title("Alarmsysteem")
root.resizable(0, 0)
root.configure(background="#ebedeb")

searchString = []
informationLabels = ["IP Adres: ", "Port: ", "Action Handler: ", "UUID: "]
informationHeaders = ["General Information", "Events"]
informationContainer = Frame()

client_list = [
    ClientNode('102.168.42.2', 5555, 'test1', None),
    ClientNode('102.168.42.3', 5555, 'test1', None),
    ClientNode('102.168.42.4', 5555, 'test1', None),
    ClientNode('102.168.42.5', 5555, 'test1', None),
    ClientNode('102.168.42.6', 5555, 'test1', None),
    ClientNode('102.168.42.7', 5555, 'test1', None),
]


def buttonClick():
    global staataan
    staataan = False if staataan else True
    print(staataan)

    if staataan:
        button.configure(bg = "red")
        button.configure(text= "      Server Disabled      ")
    else:
        button.configure(bg = "green")
        button.configure(text= "      Alarm Set     ")

def get_client_specifics(x):
    client_input = x.widget.get(x.widget.curselection()[0])
    print(client_input)
    client_info = []
    client = None

    for found_client in client_list:
        if found_client.ip_address.lower() == client_input.lower():
            client = found_client

    client_info.append(client.ip_address)
    client_info.append(client.port)
    client_info.append(client.connection_handler)
    client_info.append(client.uuid)

    informationContainer.place(relx=0.520, rely=0.15, relwidth=0.45, relheight=0.80)
    informationContainer.configure(background="white")
    informationContainer.configure(relief=FLAT)
    # informationContainer.configure(highlightbackground="black")
    # informationContainer.configure(highlightcolor="black")
    informationContainer.configure(width=500)
    informationContainer.configure(height=100)

    rely = 0
    for label in informationHeaders:
        informationContainer.tempLabel = Label(informationContainer)
        informationContainer.tempLabel.place(relx=0, rely=rely, relwidth=1, relheight=0.15)
        informationContainer.tempLabel.configure(text=label)
        informationContainer.tempLabel.configure(background="white")
        informationContainer.tempLabel.configure(font="Helvetica 12 bold")

        rely += 0.575

    rely = 0.15
    for label in range(len(informationLabels)):
        informationContainer.tempLabel = Label(informationContainer)
        informationContainer.tempLabel.place(relx=0.05, rely=rely, relwidth=0.425)
        informationContainer.tempLabel.configure(background="white")
        informationContainer.tempLabel.configure(text=informationLabels[label])
        informationContainer.tempLabel.configure(anchor='w')

        informationContainer.tempLabel = Label(informationContainer)
        informationContainer.tempLabel.place(relx=0.5, rely=rely, relwidth=0.455)
        informationContainer.tempLabel.configure(anchor='w')
        informationContainer.tempLabel.configure(background="white")
        informationContainer.tempLabel.configure(text=client_info[label])
        rely += 0.085

    if button.bg == "green":
        root.button.configure(bg = "red")
    else:
        root.button.configure(bg = "green")


root.informationContainer = Frame()
root.mechanicListBox = Listbox()
root.mechanicListBox.place(relx=0.020, rely=0.15, relwidth=0.45, relheight=0.80)
root.mechanicListBox.configure(background="white")
root.mechanicListBox.configure(relief=FLAT)
root.mechanicListBox.configure(highlightcolor="#ffffff")
root.mechanicListBox.configure(width=500)
root.mechanicListBox.configure(height=100)
root.mechanicListBox.bind("<Double-Button-1>", get_client_specifics)

#temp
for client in client_list:
    root.mechanicListBox.insert(END, client.ip_address)

button = Button(root, text = "      Alarm Set     " if staataan else "      Server Disabled      ", bg = "green" if
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


button = Button(root, text = "      Alarm Set     " if staataan else "      Alarm Disabled      ", bg = "green" if staataan else "red", command = buttonClick)
button.grid(row=0,column=0)
button.config(font=("Courier", 11))

label = Label(root, text = "Status Alarm:\n" + ("ATTENTIE: ER GAAT EEN ALARM AF" if serverbool else "GEEN BIJZONDERHEDEN"))

label.grid(row=0,column=1,padx=300)
label.config(font=("Courier", 11))

mainloop()
