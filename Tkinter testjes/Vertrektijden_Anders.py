from tkinter import *
import os, xmltodict, requests


# from PIL import Image, ImageTk

def request():
    'Stuurt een request naar de server van NS en returnt een XML'
    global station
    station = invoerVeld.get()
    auth_details = ('remcotaal@hotmail.com', 'Euclf-6uz8iWdUOl7LpERmknqv4u5IEY1Wr3hC2pkK3rJQnum3aNLg')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + station
    response = requests.get(api_url, auth=auth_details)
    return response.text

def start():
    dictionary = xmltodict.parse(request())

    if 'error' not in dictionary:  # De XML bevat een dictionary error wanneer een verkeerde waarde wordt ingevuld
        amount = 1
        spacing = 20
        for tijd in dictionary['ActueleVertrekTijden']['VertrekkendeTrein']:
            vertrekTijd = tijd['VertrekTijd']
            vertrekTijd = vertrekTijd[11:19]
            treinSoort = tijd['TreinSoort']
            eindbestemming = tijd['EindBestemming']
            label1 = Label(root,text='Het begin station is: {} {:9} {} uur De eindbestemming is: {}'.format(station.capitalize(),treinSoort, vertrekTijd,eindbestemming)).place(x=1000, y=40 + (spacing * amount))
            amount +=1
    else:
        foutcode = dictionary['error']['message']
        textVeld.insert(0, foutcode)
        request()

def hoofdframe():
    pass


def knop1():
    global root
    root.destroy()
    os.system('Beginscherm.py')



root = Tk()  # Maakt het venster

invoerVeld = StringVar()

hoofdframe = Frame(master=root,  # Venster gele gedeelte
                   background='#FFD720',
                   width=10000,
                   height=711)
hoofdframe.pack(side='top', fill=X)

onderframe = Frame(master=root,  # Venster blauwe gedeelte
                   background='#001F6A',
                   width=850,
                   height=90)
onderframe.pack(side='bottom', fill=X)

welkomlabel = Label(master=hoofdframe,  # Welkom bij NS tekst
                    text='Welkom bij NS',
                    foreground='#001F6A',
                    background='#FFD720',
                    font=('Helvetica', 30, 'bold'),
                    width=14,
                    height=3)
welkomlabel.place(x=600, y=50)

photo = PhotoImage(file='kaartlezer.PNG')  # Foto kaartlezer
fotolabel = Label(master=hoofdframe, image=photo)
fotolabel.place(x=560, y=220)

button1 = Button(master=hoofdframe,  # Knop 1
                 text="Ga terug naar\n beginscherm",
                 foreground="white",
                 background="#001F6A",
                 font=('arial', 12, 'bold'),
                 width=17,
                 height=3,
                 command=knop1)
button1.place(x=380, y=500)

button2 = Button(master=hoofdframe,                                 #Knop 2
                 text="Gaan met die\n banaan",
                 foreground="white",
                 background="#001F6A",
                 font=('arial', 12, 'bold'),
                 width=17,
                 height=3,
                 command=start)
button2.place(x=580, y=500)

mEntry = Entry(root,textvariable=invoerVeld).place(x = 50,y=50)


root.mainloop()
