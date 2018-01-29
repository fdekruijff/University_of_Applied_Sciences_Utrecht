from tkinter import *
import os, xmltodict, requests



def knop1():
    'Open GUI huidig station'
    global root
    root.destroy()
    os.system('Huidig_Station.py')

def knop2():
    'Open GUI ander station'
    global root
    root.destroy()
    os.system('Ander_Station.py')


def nl_to_eng():
    'Wanneer er op de Engelse vlag wordt gedrukt veranderd de Nederlandstalige tekst naar het Engels'
    button1['text'] = 'Departure\ntimes current station'
    button2['text'] = 'Departure\ntimes other station'
    welkomlabel['text'] = 'Welcome to NS'
    photo['file'] = 'afbeeldingen\kaartlezerengels.PNG'


def eng_to_nl():
    'Wanneer er op de Nederlandse vlag wordt gedrukt veranderd de Engelstalige tekst naar het Nederlands'
    button1['text'] = 'Actuele vertrektijden\nhuidig station'
    button2['text'] = 'Actuele vertrektijden\nander station'
    welkomlabel['text'] = 'Welkom bij NS'
    photo['file'] = 'afbeeldingen\kaartlezer.PNG'

root = Tk() # Maakt het venster
root.attributes('-fullscreen',True)         #Open fullscreen


hoofdframe = Frame(master=root,             #Venster gele gedeelte
                   background='#FFD720',
                   width=1920,
                   height=980)
hoofdframe.pack(side='top', fill=X)

onderframe = Frame(master=root,             #Venster blauwe gedeelte
                   background='#001F6A',
                   width=1920,
                   height=100)
onderframe.pack(side='bottom', fill=X)


welkomlabel = Label(master=hoofdframe,                        #Welkom bij NS tekst
                    text='Welkom bij NS',
                    foreground='#001F6A',
                    background='#FFD720',
                    font=('Helvetica', 60, 'bold'),
                    width=14,
                    height=3)
welkomlabel.place(x=615, y=50)



photo = PhotoImage(file='afbeeldingen\kaartlezer.PNG')               #Foto kaartlezer
fotolabel = Label(master=hoofdframe, image=photo, borderwidth=-1)
fotolabel.place(x=745, y=320)


button1 = Button(master=hoofdframe,                                 #Knop 2
                 text="Actuele vertrektijden\nhuidig station",
                 foreground="white",
                 background="#001F6A",
                 font=('arial', 12, 'bold'),
                 width=17,
                 height=3,
                 command=knop1)
button1.place(x=765, y=650)

button2 = Button(master=hoofdframe,                                 #Knop 3
                 text="Actuele vertrektijden\nander station",
                 foreground="white",
                 background="#001F6A",
                 font=('arial', 12, 'bold'),
                 width=17,
                 height=3,
                 command=knop2)
button2.place(x=965, y=650)


buttonNL = Button (master=onderframe,                               #Knop van Engels naar Nederlands
                   width=10,
                   height=10,
                   command=eng_to_nl)
photoNL = PhotoImage (file='afbeeldingen\kroodwitblauw.png')
buttonNL.config(image=photoNL,                                      #Het converteren dat de afbeelding een knop wordt
                width=48,
                height=25)
buttonNL.place(x=50, y=25)

labelengels = Label(master=onderframe,                              #Label onder de Engelse vlag
                    text='English',
                    foreground='white',
                    background='#001F6A',
                    font=('arial', 9))
labelengels.place(x=128, y=55)

buttonENG = Button (master=onderframe,                              #Knop van Nederlands naar Engels
                   width=10,
                   height=10,
                    command=nl_to_eng)
photoENG = PhotoImage (file='afbeeldingen\kengenland.png')
buttonENG.config(image=photoENG,                                    #Het converteren dat de afbeelding een knop wordt
                width=48,
                height=25)
buttonENG.place(x=125, y=25)

labelnederlands = Label(master=onderframe,                          #Label onder de Nederlandse vlag
                        text='Nederlands',
                        foreground='white',
                        background='#001F6A',
                        font=('arial', 9))
labelnederlands.place(x=42, y=55)

root.mainloop()
