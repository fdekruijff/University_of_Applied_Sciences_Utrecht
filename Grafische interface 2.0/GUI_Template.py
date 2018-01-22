import csv
import requests
import tkinter.font
from tkinter import *
import uuid

UUID = "GUI" + uuid.uuid4().hex

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
    'Kering sluiten'
    label4['fg'] = 'red'
    label4['text'] = 'GESLOTEN'
    #button2['state'] = 'disabled'
    #button3['state'] = 'active'

def button3():
    'Kering openen'
    label4['fg'] = 'green'
    label4['text'] = 'OPEN'
    #button3['state'] = 'disabled'
    #button2['state'] = 'active'





bestandLocatie = 'Waterpeil.csv'

root = Tk()



my_font = tkinter.font.Font(family="Courier", size=9)
my_font2 = tkinter.font.Font(family="Courier", size=12)

root.resizable(width=False, height=False)
root.minsize(width=800, height=600)
root.maxsize(width=800, height=600)

hoofdframe = Frame(master=root, #Maakt hoofdframe aan
                   background='midnight blue',
                   highlightthickness=15,
                   highlightbackground='DodgerBlue4',
                   highlightcolor='DodgerBlue4'
                   )
hoofdframe.pack(side=LEFT, fill=BOTH, expand=True)

resultaatframe = Frame(master=root, #Maakt resultaatframe aan
                       width=250,
                       height=250,
                       background='midnight blue',
                       highlightthickness=15,
                       highlightbackground='DodgerBlue4',
                       highlightcolor='DodgerBlue4'
                       )
resultaatframe.pack(side=BOTTOM)

scrollbar = Scrollbar(master=resultaatframe, width=25)
scrollbar.pack(side=RIGHT, fill=Y)


button1 = Button(master=resultaatframe, text='VERVERS GEGEVENS', command=button1)
button1.pack(side=BOTTOM, fill=X)


textVeld = Listbox(master=resultaatframe,                       #Listbox om resultaten csv weer te geven
                   bd=5,
                   width=55,
                   font=my_font,
                   height=26,
                   )

textVeld.pack(side=BOTTOM)

bovenframe = Frame(master=root,     #Maakt resultaatframe aan
                   background='midnight blue',
                   highlightthickness=15,
                   highlightbackground='DodgerBlue4',
                   highlightcolor='DodgerBlue4'
                   )
bovenframe.pack(side=TOP, fill=BOTH, expand=True)

textVeld.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textVeld.yview)

label7 = Label(master=hoofdframe, text="Raspberry 1:", bg='midnight blue', fg='white', font=my_font2)
label7.grid(row=0, column=0)

label8 = Label(master=hoofdframe, text="Operationeel", bg='midnight blue', fg='white', font=my_font2)
label8.grid(row=1, column=0)

label9 = Label(master=hoofdframe, text='', bg='midnight blue', fg='white', font=my_font2)
label9.grid(row=2, column=0)

label10 = Label(master=hoofdframe, text='Raspberry 2:', bg='midnight blue', fg='white', font=my_font2)
label10.grid(row=3, column=0)

label11 = Label(master=hoofdframe, text="Operationeel", fg='white', bg='midnight blue', font=my_font2)
label11.grid(row=4, column=0)




#button2 = Button(master=hoofdframe, text='Waterkering sluiten', bd=1, command=button2)
#button2.grid(row=5, column=0)

#button3 = Button(master=hoofdframe, text='Waterkering openen', bd=1, command=button3, state='disabled')
#button3.grid(row=5, column=1)





label1 = Label(master=bovenframe, text="Status:", bg='midnight blue', fg='white', font=my_font2)
label1.grid(row=0, column=0, sticky=W)

label2 = Label(master=bovenframe, text="In werking", bg='midnight blue', fg='white', font=my_font2)
label2.grid(row=0, column=1)

label3 = Label(master=bovenframe, text="Kering:", bg='midnight blue', fg='white', font=my_font2)
label3.grid(row=1, column=0, sticky=W)

label4 = Label(master=bovenframe, text="OPEN", fg='green', bg='midnight blue', font=my_font2)
label4.grid(row=1, column=1, sticky=W)

label5 = Label(master=bovenframe, text="Waterpeil:", bg='midnight blue', fg='white', font=my_font2)
label5.grid(row=2, column=0)

label6 = Label(master=bovenframe, text="{} meter".format('3.5'), fg='white', bg='midnight blue', font=my_font2)
label6.grid(row=2, column=1, sticky=W)


root.mainloop()