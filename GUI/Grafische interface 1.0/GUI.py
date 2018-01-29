import csv
import requests
import tkinter.font
from tkinter import *

CSV_URL = 'https://waterberichtgeving.rws.nl/wbviewer/maak_grafiek.php?loc=HOEK&set=eindverwachting&nummer=1&format=csv'

def haal_gegevens_op():
    "Haalt gegevens op en schrijft dit weg in een csv bestand"
    with requests.Session() as s:   #Haalt gegevens op van de server
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        lezen = csv.reader(decoded_content.splitlines(), delimiter=';')
        lijst = list(lezen)


    with open(bestandLocatie, 'w', newline='') as myCSVFile:    #Schrijft gegevens weg in csv bestand
        schrijven = csv.writer(myCSVFile, delimiter=';')

        for lijn in lijst:
            schrijven.writerow(lijn)

def toon_gegevens():
    'Zet de gegevens in een listbox met een bijbehorende kleur'
    with open(bestandLocatie, 'r') as myCSVFILE:  # Leest het geschreven csv bestand
        textVeld.delete(0, END)
        reader = csv.reader(myCSVFILE, delimiter=';')
        index = 2

        textVeld.insert(0, '{:19}{:15}{:21}{:18}{:4}'.format('Datum/tijd (MET)', '|Astronomisch', '|Gemeten waterstand',
                                                              '|Verwachte opzet', '|Verwachting RWS'))
        textVeld.insert(1, '{:19}|{:14}|{:20}|{:17}|{:4}'.format('','','','',''))
        myCSVFILE.readline()

        for lijn in reader:  # Elke lijn met waardes komt in een tuple
            datum = lijn[0]
            astronomisch = lijn[1]
            waterstand = lijn[2]
            opzet = lijn[3]
            verw_RWS = lijn[4]



            textVeld.insert(index, '{:19}|{:14}|{:20}|{:17}|{:4}'.format(datum, astronomisch, waterstand, opzet, verw_RWS))
            if int(opzet) >= 30:
                textVeld.itemconfig(index, {'fg': 'red'})
            elif int(opzet) >= 20 and int(opzet) < 30:
                textVeld.itemconfig(index, {'fg': 'orange'})
            else:
                textVeld.itemconfig(index, {'fg': 'green'})

            index += 1

def button1():
    #haal_gegevens_op()
    toon_gegevens()

def button2():
    label2['fg'] = 'red'
    label2['text'] = 'GESLOTEN'
    button2['state'] = 'disabled'
    button3['state'] = 'active'

def button3():
    label2['fg'] = 'green'
    label2['text'] = 'OPEN'
    button3['state'] = 'disabled'
    button2['state'] = 'active'





bestandLocatie = 'Waterpeil.csv'

root = Tk()

my_font = tkinter.font.Font(family="Courier", size=9)

root.resizable(width=False, height=False)
root.minsize(width=800, height=666)
root.maxsize(width=800, height=666)

scrollbar = Scrollbar(master=root, width=20)
scrollbar.pack(side=RIGHT, fill=Y)

hoofdframe = Frame(master=root, #Maakt hoofdframe aan
                   width=125,
                   height=666,)
hoofdframe.pack(side=LEFT, fill=BOTH)

resultaatframe = Frame(master=root, #Maakt resultaatframe aan
                       width=655,
                       height=666)
resultaatframe.pack(side=RIGHT)



textVeld = Listbox(master=resultaatframe,                       #Listbox om resultaten csv weer te geven
                   bd=5,
                   width=150,
                   font=my_font,
                   height=39)

textVeld.pack(side=TOP)

textVeld.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textVeld.yview)


button1 = Button(master=resultaatframe, text='VERVERS GEGEVENS', bd=1, command=button1)
button1.pack(side=BOTTOM, fill=X)

button2 = Button(master=hoofdframe, text='Waterkering sluiten', bd=1, command=button2)
button2.pack(side=BOTTOM, fill=X)

button3 = Button(master=hoofdframe, text='Waterkering openen', bd=1, command=button3)
button3.pack(side=BOTTOM, fill=X, pady=5)





label1 = Label(master=hoofdframe, text="Status waterkering")
label1.pack(side=TOP, fill=X)

label2 = Label(master=hoofdframe, text="", fg='green')
label2.pack(side=TOP, fill=X, pady=5)




root.mainloop()