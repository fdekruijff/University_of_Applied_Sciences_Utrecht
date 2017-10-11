import datetime
from Mechanic import Mechanic
from CardMachine import  CardMachine


class Notification:
    def __init__(self, time, message):
        self.time = time.strftime("%d-%m-%Y %H:%M")
        self.message = message
