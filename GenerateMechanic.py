"""
    Project: Mini project TICT-V1PROG-15
    School: Hogeschool Utrecht B HBO-ICT
"""

import random
import names
import requests
from Mechanic import Mechanic


class GenerateMechanic:
    regions = {
        "drenthe": {"lat": 52.9476012, "long": 6.623058600000036},
        "flevoland": {"lat": 52.5279781, "long": 5.595350800000006},
        "friesland": {"lat": 53.1641642, "long": 5.781754200000023},
        "gelderland": {"lat": 52.045155, "long": 5.871823500000005},
        "groningen": {"lat": 53.2193835, "long": 6.566501700000003},
        "limburg": {"lat": 51.4427238, "long": 6.060872600000039},
        "noord-brabant": {"lat": 51.4826537, "long": 5.232168699999988},
        "noord-holland": {"lat": 52.5205869, "long": 4.788473999999951},
        "overijssel": {"lat": 52.4387814, "long": 6.501641100000029},
        "utrecht": {"lat": 52.09073739999999, "long": 5.121420100000023},
        "zeeland": {"lat": 51.4940309, "long": 3.849681499999974},
        "zuid-holland": {"lat": 52.0207975, "long": 4.493783600000029}
    }

    @staticmethod
    def get_address_from_coordiantes(lat, long):
        """ Reverse geocoding """
        base = "https://maps.googleapis.com/maps/api/geocode/json?"
        params = "latlng={lat},{lon}&sensor={sen}&key={key}".format(
            lat=lat,
            lon=long,
            sen='true',
            key='AIzaSyDQJhy23ZFqmyD7Xq8a3GlvAopxD-6g_HM'
        )

        response = requests.get("{base}{params}".format(base=base, params=params))
        try:
            return response.json()['results'][0]['formatted_address']
        except IndexError:
            return -1

    @staticmethod
    def check_coordinates_in_province(lat, long, province):
        """ Reverse geocoding """
        base = "https://maps.googleapis.com/maps/api/geocode/json?"
        params = "latlng={lat},{lon}&sensor={sen}&key={key}".format(
            lat=lat,
            lon=long,
            sen='true',
            key='AIzaSyDQJhy23ZFqmyD7Xq8a3GlvAopxD-6g_HM'
        )

        response = requests.get("{base}{params}".format(base=base, params=params))
        try:
            response = response.json()['results'][0]['address_components'][4]['long_name']
        except IndexError:
            return False
        if response.lower() == province.lower():
            return True
        return False

    @staticmethod
    def generate_coordinates(input_latitude, input_longitude):
        while True:
            new_latitude = random.uniform(input_latitude - random.uniform(-1, 1),
                                          input_latitude + random.uniform(-1, 1))
            new_longitude = random.uniform(input_longitude - random.uniform(-1, 1),
                                           input_longitude + random.uniform(-1, 1))

            return new_latitude, new_longitude

    @staticmethod
    def generate_mechanic(province: str):
        if random.uniform(0, 1) <= 0.5:
            name = names.get_full_name(gender='male')
            gender = 'male'
        else:
            # Female
            name = names.get_full_name(gender='female')
            gender = 'female'
#shifts
        if random.uniform(0, 1) <= 0.5:
            shift = 'day'
        else:
            shift = 'night'

        age = random.randint(21, 65)

        coordinates = GenerateMechanic.generate_coordinates(
            GenerateMechanic.regions[province.lower()]['lat'],
            GenerateMechanic.regions[province.lower()]['long']
        )

        return Mechanic(name, gender, age, coordinates[0], coordinates[1], province, None, "Available",shift)
