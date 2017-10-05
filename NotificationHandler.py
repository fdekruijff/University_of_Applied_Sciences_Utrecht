import datetime
from Mechanic import Mechanic
from CardMachine import  CardMachine


class NotificationHandler:
    @staticmethod
    def new_notification(controller, timestamp: datetime, message, card_machine, mechanic):
        # first format the notification
        time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

