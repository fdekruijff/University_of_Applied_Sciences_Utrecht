import datetime
from Mechanic import Mechanic
from CardMachine import  CardMachine


class Notification:
    def __init__(self, time, message):
        self.time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.message = message
