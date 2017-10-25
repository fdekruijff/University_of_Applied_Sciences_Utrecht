# TICT-V1CSN-15 Miniproject

This is the final project for the course TICT-V1CSN-15 for the University of Applied Sciences in Utrecht. The goal of this project is to make a client-server security system with Raspberry Pi's

## Getting Started

The instructions will get you set up on the hardware and software side of this project.

### Prerequisites

For this project are no additional prerequisites required.

### Installing Software

Follow these steps to get the software running on your nodes.

1. Clone server.py to your server node

```
wget https://github.com/fdekruijff/TICT-V1CSN-15-Miniproject/blob/master/server.py
```

2. Clone client.py to your server node

```
wget https://github.com/fdekruijff/TICT-V1CSN-15-Miniproject/blob/master/client.py
```

3. Make sure your server node has a DHCP server running in the range of 192.168.42.1/24
4. Make sure your firewalls accept port 5555
5. Run server.py on your server

```
python3 /path/to/file/server.py
```

6. Run client.py on your client / clients

```
python3 /path/to/file/client.py
```

## Getting the hardware wired up

Will be added in the future.


## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE for Professional Developers by JetBrains
* [Raspberry Pi](https://www.raspberrypi.org/) - General Purpose Input Output single-board computer

## Authors

* **Floris de Kruijff** - *Sockets, Network* - [fdekruijff](https://github.com/fdekruijff)
* **Bryan Campagne** - *GPIO, Hardware* - [Joepieler](https://github.com/Joepieler)
* **Rik van Velzen** - *TkInter, GUI* - [Rikvanvelzen](https://github.com/Rikvanvelzen)

See also the list of [contributors](https://github.com/fdekruijff/TICT-V1CSN-15-Miniproject/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* README.md [template](https://gist.githubusercontent.com/PurpleBooth/109311bb0361f32d87a2/raw/824da51d0763e6855c338cc8107b2ff890e7dd43/README-Template.md)