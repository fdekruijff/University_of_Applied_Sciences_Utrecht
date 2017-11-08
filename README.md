# TICT-V1PROG-15 Miniproject

This is the final project for the course TICT-V1PROG-15 for the University of Applied Sciences in Utrecht. The goal of this project is to make a GUI to display API data based on Station data and Mechanics.

## Getting Started

The instructions will get you set up to run this project yourself.

### Prerequisites

The following python modules need to be imported
* ```python -m pip install pypiwin32```
* ```python -m pip install googlemaps```
* ```python -m pip install twilio```
* ```python -m pip install pyyaml```

### Installing Software

To run the program please follow these steps:

1. Clone the GitHub repository

```
git clone https://github.com/fdekruijff/TICT-V1PROG-15-Miniproject.git NSDefectOverview
```

2. Change directory

```
cd ./NSDefectOverview/
```


3. Run Main.py
```
C:\path\to\python3.exe Main.py
```

## You should see this

If everything worked you should see the following window appear. Congratulations everything is working now.

![program homescreen](https://image.prntscr.com/image/akI1x-zIRRevKVh0IZQfvQ.png)

##  Program Structure
```
/NSDefectOverview
    |-- Main.py
    |-- NSDefectOverview.py
    |__ /classes
         |-- __init__.py
         |-- CardMachine.py               
         |-- GenerateMechanic.py               
         |-- Mechanic.py               
         |-- Notification.py               
         |-- PopulateDataLists.py               
         |-- RandomCardMachineDefect.py               
     |__ /images
         |-- ns_logo_1.png
         |-- ns_logo_1_25.png
         |-- ns_logo_1_50.png  
     |__ /pages
         |-- __init__.py
         |-- CardMachineOverviewPage.py  
         |-- MechanicsOverviewPage.py  
         |-- NotificationPage.py  
         |-- StartPage.py  
    |-- .gitignore
    |-- README.md
    |-- LICENCE.txt
    |-- CHANGES.txt
```
## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE for Professional Developers by JetBrains
* [NS API](https://www.ns.nl/reisinformatie/ns-api) - API to get Dutch train station information
* [Google API](https://developers.google.com/maps/) - Google Maps API to get distance and travel time between coordinates
* [Twilio API](https://www.twilio.com/) - Platform to send text messages

## Authors

* **Floris de Kruijff** - *TkInter logic* - [fdekruijff](https://github.com/fdekruijff)
* **Bryan Campagne** - *XML / SQLite logic* - [Joepieler](https://github.com/Joepieler)
* **Rik van Velzen** - *API logic* - [Rikvanvelzen](https://github.com/Rikvanvelzen)

See also the list of [contributors](https://github.com/fdekruijff/TICT-V1CSN-15-Miniproject/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* README.md [template](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/824da51d0763e6855c338cc8107b2ff890e7dd43/README-Template.md)