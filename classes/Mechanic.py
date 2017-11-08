"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import xml.etree.ElementTree as Et
import sqlite3
from classes.GenerateMechanic


class Mechanic:
    """
        This class holds information for the mechanics. Mechanic objects are used throughout the program to display and
        modify data.
    """
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
        self.conn = sqlite3.connect('nsdefect.db')
        self.c = conn.cursor()

    def __str__(self):
        """ str() used to display all class attributes (but not their values). """
        return ''.join([key + ', ' for key in vars(self)])

    def set_attribute(self, attribute: str, value: str, mechanic_xml_file: str):
        """
            Generic function to modify either one of the attributes, updates the associated XML
            file with the new data as well
        """
        # First make sure the new attribute data is in the correct format.
        if Mechanic.check_attribute_format(attribute, value):
            try:
                setattr(self, attribute, value)  # Update the instance attribute.
            except AttributeError:
                return False

            # Parse and update the associated XML file to save changes even if program goes offline.
            tree = Et.parse(mechanic_xml_file)
            for x in tree.getroot():
                found = False
                for meta in x:
                    if meta.text.lower() == self.name.lower():
                        found = True

                    if meta.tag.lower() == attribute.lower() and found:
                        meta.text = value
                        self.c.execute("Update mechanics SET '{}'='{}' WHERE name = '{}'".format(attribute, value, self.name))
            # Write XML changes back to the file
            tree.write(mechanic_xml_file)
            return True
        return False

    # Remove this Mechanic instance from the XML file.
    def remove(self, mechanic_xml_file):
        tree = Et.parse(mechanic_xml_file)
        for x in tree.getroot():
            for meta in x:
                if meta.text.lower() == self.name.lower():
                    # The XML Element is found in the tree. Get its root and delete it.
                    tree.getroot().remove(x)
                    self.c.execute("DELETE FROM mechanics WHERE name = '{}'".format(self.name))
        tree.write(mechanic_xml_file)

    @staticmethod
    def check_attribute_format(attribute, value):
        """
            Make sure the new attribute data is correct so it doesn't break the rest of the program.
            Only a few attributes need to be in a specified format.

            Check if correct data returns True.
            >>> Mechanic.check_attribute_format("region", "noord-holland")
            True

             Check if wrong data returns False.
            >>> Mechanic.check_attribute_format("shift", "dusk")
            False
         """
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
