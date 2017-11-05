"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""


class Notification:
    """ Class for Notification instances. """
    def __init__(self, time, message):
        self.time = time.strftime("%d-%m-%Y %H:%M")
        self.message = message
