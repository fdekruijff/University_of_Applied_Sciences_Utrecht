"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import uuid


class CardMachine:
    """ Class for CardMachine instances based on NS API station data. """
    def __init__(self, station_name, longitude, latitude):
        self.station_name = station_name
        self.longitude = longitude
        self.latitude = latitude
        self.uuid = uuid.uuid4().hex
        self.defect = "Operational"
