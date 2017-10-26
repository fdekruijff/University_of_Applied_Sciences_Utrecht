class Notification:
    def __init__(self, time, message):
        self.time = time.strftime("%d-%m-%Y %H:%M")
        self.message = message
