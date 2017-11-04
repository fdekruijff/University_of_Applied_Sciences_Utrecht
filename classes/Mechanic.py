"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import xml.etree.ElementTree as Et


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

    def set_attribute(self, attribute: str, value: str, mechanic_xml_file: str):
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
