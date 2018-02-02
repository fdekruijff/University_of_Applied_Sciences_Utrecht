# TICT-V1IDP-15 Interdisciplinair Project

Deze repository bevat onze uitwerking van  het Interdisciplinaire Project.  

Ons doel was om een proof of concept te maken van de maeslantkering waar de vier disciplines van ICT terug in voor komen. Dit heeft zich geuit in een houte fysiek model en de code die te vinden is in deze repository.

## Beginnen

Om de code van dit project werkend te krijgen moet je simpelweg de volgende stappen volgen.

### Precondities

De volgende onderdelen zijn nodig voor dit project:
- 3x Raspberry Pi's
- 1x LCD1602
- 1x DC Stappen motor
- 1x Ultrasonic Sensor HC-SR04
- 1x 3-way switch
- 4x UTP kabels
- 1x Switch

### Installeren software

Het installeren van de software op de Raspberry Pi's vereist de volgende stappen:

1.0. Installeer [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) op de drie Raspberry Pi's  
2.0. Geef de Raspberry Pi's statische IP addressen

#### Server
Op de Server Raspberry Pi:  
3.1 ``` mkdir /home/pi/Desktop/codebase ```  
3.2 ``` git clone https://github.com/RemcoTaal/TICT-V1IDP-15-Miniproject.git /home/pi/Desktop/codebase```

#### Clients
Op de twee Client Raspberry Pi:  
4.1 ``` mkdir /home/pi/Desktop/codebase ```  
4.2 ``` git clone https://github.com/RemcoTaal/TICT-V1IDP-15-Miniproject.git /home/pi/Desktop/codebase```

#### GUI
Op een willekeurige computer, in hetzelfde netwerk als de Server  
5.1 ``` git clone https://github.com/RemcoTaal/TICT-V1IDP-15-Miniproject.git ```

6.0 Vervolgens is moeten de raspberry Pi's aangesloten worden volgens het schakelschema, Node 2 hoeft in principe niet op GPIO aangesloten te worden.

7.0 Om alles uit te voeren:  
7.1 Server PI > python3 Server.py  
7.2 Node 1 PI > python3 BarrierNode.py (IP=IP van server, UUID=NODE_1, Poort=5555)  
7.2 Node 2 PI > python3 BarrierNode.py (IP=IP van server, UUID=NODE_2, Poort=5555)  
7.3 GUI > python3 Gui.py (IP=IP van server)

## Aansluiten van de hardware

Het volgende schema laat zien hoe de Raspberry Pi's moeten worden aangesloten om de software te laten werken.

![wiring scheme](https://image.prntscr.com/image/GMsZFkp4TRqVMKpiuWYHRA.png)

## Gemaakt met

* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE for Professional Developers door JetBrains
* [Raspberry Pi](https://www.raspberrypi.org/) - General Purpose Input Output single-board computer
* [Hogeschool Utrecht](https://www.hu.nl) - Hardware TI Lab Hogeschool Utrecht
## Auteurs

* **Floris de Kruijff** - *Technische Informatica* - *Sockets, TkInter* - [fdekruijff](https://github.com/fdekruijff)
* **Bryan Campagne** - *Technische Informatica* - *GPIO, LCD, DC Motor* - [Joepieler](https://github.com/Joepieler)
* **David Cramer** - *Technische informatica* - *GPIO, Water sensor, logica* - [paggaboi](https://github.com/paggaboi)
* **Rik van Velzen** - *Business & IT management* - *Documentatie, adviezen* - [Rikvanvelzen](https://github.com/Rikvanvelzen)
* **Remco Taal** - *Software & Information Engineering* - *TkInter, GUI* - [RemcoTaal](https://github.com/RemcoTaal)

## Licentie

Dit project valt onder de MIT licentie - zie [LICENSE.md](LICENSE.md) voor details

## Erkenning

* README.md [template](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/824da51d0763e6855c338cc8107b2ff890e7dd43/README-Template.md)
