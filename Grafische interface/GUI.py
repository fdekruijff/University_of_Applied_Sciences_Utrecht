import csv
from tkinter import *

bestandLocatie = 'Waterpeil.csv'

root = Tk()
root.resizable(width=False, height=False)
root.minsize(width=800, height=666)
root.maxsize(width=800, height=666)

hoofdframe = Frame(master=root,
                   width=125,
                   height=666)
hoofdframe.pack(side=LEFT)

resultaatframe = Frame(master=root,
                       width=900,
                       height=980)
resultaatframe.pack(side=RIGHT)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)






textVeld = Listbox(master=resultaatframe,                       #Listbox om resultaten csv weer te geven
                   bd=5,
                   width=150,
                   font=('arial', 9, 'bold'),
                   height=39)

textVeld.pack(side=TOP)



button1 = Button(master=resultaatframe, text='VERVERS GEGEVENS')
button1.pack(side=BOTTOM, fill=X)



label1 = Label(master=hoofdframe, text="Status waterkering")
label1.place(x=10, y=0)

label2 = Label(master=hoofdframe, text="OPEN", fg='green')
label2.place(x=40, y=25)

label3 = Label(master=hoofdframe, text="Status waterkering")
label3.place(x=10, y=50)

label4 = Label(master=hoofdframe, text="GESLOTEN", fg='red')
label4.place(x=35, y=75)



with open(bestandLocatie, 'r') as myCSVFILE:                #Leest het geschreven csv bestand
    reader = csv.reader(myCSVFILE, delimiter=';')
    index = 2

    textVeld.insert(0, '{:25}{:18}{:30}{:30}{:30}'.format('Datum/tijd (MET)', 'Astronomisch', 'Gemeten waterstand','Verwachte opzet','Verwachting RWS'))
    textVeld.insert(1, '')
    myCSVFILE.readline()

    for lijn in reader:  # Elke lijn met waardes komt in een tuple
        textVeld.insert(index, '{:25} {:30} {:50} {:50} {:50}'.format(lijn[0], lijn[1], lijn[2], lijn[3], lijn[4]))
        index += 1


textVeld.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textVeld.yview)

root.mainloop()
