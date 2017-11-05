"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import xml.etree.ElementTree as Et
try:
    from classes.GenerateMechanic import GenerateMechanic
except ImportError:
    pass

class Mechanic:
    def __init__(self, name, gender, age, latitude, longitude, region, schedule, availability, shift, phone):
        self.name = name
        self.gender = gender
        self.age = age
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.schedule = schedule
        self.availability = availability
        self.shift = shift
        self.phone_number = phone

    def __str__(self):
        return ''.join([key + ', ' for key in vars(self)])

    def set_attribute(self, attribute: str, value: str, mechanic_xml_file: str):
        if Mechanic.check_attribute_format(attribute, value):
            try:
                setattr(self, attribute, value)
            except AttributeError:
                return False

            tree = Et.parse(mechanic_xml_file)
            for x in tree.getroot():
                found = False
                for meta in x:
                    if meta.text.lower() == self.name.lower():
                        found = True

                    if meta.tag.lower() == attribute.lower() and found:
                        meta.text = value

            tree.write(mechanic_xml_file)
            return True
        return False

    def remove(self, mechanic_xml_file):
        tree = Et.parse(mechanic_xml_file)
        for x in tree.getroot():
            for meta in x:
                if meta.text.lower() == self.name.lower():
                    tree.getroot().remove(x)
        tree.write(mechanic_xml_file)

    @staticmethod
    def check_attribute_format(attribute, value):
        if attribute == "region":
            if (type(value) is str) and (value in GenerateMechanic.regions):
                return True
            return False
        elif attribute == "availability":
            if (type(value) is str) and (value is "Available") or (value is "Occupied"):
                return True
            return False
        elif attribute == "shift":
            if (type(value) is str) and (value is 'day') or (value is 'night'):
                return True
            return False
        elif attribute == "phone_number":
            if (type(value) is str) and ('+' in value):
                return True
            return False
        return True
