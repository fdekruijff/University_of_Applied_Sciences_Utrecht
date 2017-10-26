"""
    Title: Final Assignment 10
    Author: Floris de Kruijff
    Date created: 12-Oct-17
"""


import xmltodict

stations = None

with open('stations.xml', 'r') as file:
    stations = xmltodict.parse(file.read())['Stations']


print("\nDit zijn de codes en de types van de 4 stations")
for station in stations['Station']:
    print("{}  -  {}".format(station['Code'], station['Type']))


print("\nDit zijn alle stations met een of meer synoniemen")
for station in stations['Station']:
    if station['Synoniemen']:
        print("{}  -  {}".format(station['Namen']['Lang'], station['Synoniemen']))

print("\nDit is de lange naam van elk station")
for station in stations['Station']:
    print("{}  -  {}".format(station['Code'], station['Namen']['Lang']))
