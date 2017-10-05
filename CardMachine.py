"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""


import uuid


class CardMachine:
    def __init__(self, station_name, longitude, latitude):
        self.station_name = station_name
        self.longitude = longitude
        self.latitude = latitude
        self.uuid = uuid.uuid4().hex

        self.defect = "Operational"
