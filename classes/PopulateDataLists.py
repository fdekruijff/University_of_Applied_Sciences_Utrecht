"""
    Programming
    University of Applied Sciences Utrecht
    TICT-V1PROG-15 Project
"""

import requests
import os
import operator
import datetime
from classes.CardMachine import CardMachine
from classes.Mechanic import Mechanic
from classes.Notification import Notification
from classes.GenerateMechanic import GenerateMechanic
import xml.etree.ElementTree as Et


class PopulateDataLists:
    @staticmethod
    def populate_card_machine_list(ns_api_username: str, ns_api_password: str) -> list:
        return_list = []
        response = None
        try:
            response = requests.get(
                url="http://webservices.ns.nl/ns-api-stations-v2",
                auth=(ns_api_username, ns_api_password)
            )
        except requests.exceptions.ConnectionError:
            exit("Failed to establish connection with NS API, please try again.")

        for element in Et.fromstring(response.text):
            is_in_netherlands = False
            station_name = ""
            latitude = ""
            longitude = ""
            for meta in element:
                if meta.tag == "Namen":
                    for name in meta:
                        if name.tag == "Lang":
                            station_name = name.text
                if meta.text == "NL":
                    is_in_netherlands = True
                if meta.tag == "Lat":
                    latitude = meta.text
                if meta.tag == "Lon":
                    longitude = meta.text
            if is_in_netherlands:
                return_list.append(CardMachine(station_name, longitude, latitude))

        return return_list

    @staticmethod
    def populate_mechanic_list(mechanic_file):
        return_list = []
        if os.path.isfile(mechanic_file):
            if os.stat(mechanic_file).st_size == 0:
                root = Et.Element("mechanics")
                for province in GenerateMechanic.regions:
                    for amount in range(5):
                        mechanic = GenerateMechanic.generate_mechanic(province)
                        return_list.append(mechanic)

                        mec = Et.SubElement(root, "mechanic")
                        Et.SubElement(mec, "name").text = str(mechanic.name)
                        Et.SubElement(mec, "gender").text = str(mechanic.gender)
                        Et.SubElement(mec, "age").text = str(mechanic.age)
                        Et.SubElement(mec, "latitude").text = str(mechanic.latitude)
                        Et.SubElement(mec, "longitude").text = str(mechanic.longitude)
                        Et.SubElement(mec, "region").text = str(mechanic.region)
                        Et.SubElement(mec, "schedule").text = str(mechanic.schedule)
                        Et.SubElement(mec, "availability").text = str(mechanic.availability)
                        Et.SubElement(mec, "shift").text = str(mechanic.shift)
                        Et.SubElement(mec, "phone").text = str(mechanic.phone_number)
                tree = Et.ElementTree(root)
                tree.write(mechanic_file)
            else:
                tree = Et.parse(mechanic_file)
                for x in tree.getroot():
                    name = gender = age = latitude = longitude = region = schedule = availability = shift = phone = ""
                    for meta in x:
                        if meta.tag == "name":
                            name = meta.text
                        if meta.tag == "gender":
                            gender = meta.text
                        if meta.tag == "age":
                            age = int(meta.text)
                        if meta.tag == "latitude":
                            latitude = float(meta.text)
                        if meta.tag == "longitude":
                            longitude = float(meta.text)
                        if meta.tag == "region":
                            region = meta.text
                        if meta.tag == "schedule":
                            schedule = meta.text
                        if meta.tag == "availability":
                            availability = meta.text
                        if meta.tag == "shift":
                            shift = meta.text
                        if meta.tag == "phone":
                            phone = meta.text

                    return_list.append(
                        Mechanic(name, gender, age, latitude, longitude, region, schedule, availability, shift, phone)
                    )
            return_list.sort(key=operator.attrgetter('name'))
            return return_list
        else:
            open(mechanic_file, 'w')
            return PopulateDataLists.populate_mechanic_list(mechanic_file)

    @staticmethod
    def populate_notification_list(notification_file):
        return_list = []
        if os.path.isfile(notification_file):
            if os.stat(notification_file).st_size == 0:
                notifications = Et.Element("notifications")
                tree = Et.ElementTree(notifications)
                tree.write(notification_file)
            else:
                tree = Et.parse(notification_file)
                for x in tree.getroot():
                    time = message = ""
                    for meta in x:
                        if meta.tag == 'time':
                            time = meta.text
                        if meta.tag == 'message':
                            message = meta.text
                    return_list.append(Notification(datetime.datetime.strptime(
                        time, "%d-%m-%Y %H:%M"), message))
                return_list.sort(key=operator.attrgetter('time'))
            return return_list
        else:
            open(notification_file, 'w')
            return PopulateDataLists.populate_notification_list(notification_file)
