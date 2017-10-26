"""
    Title: Final Assignment 8
    Author: Floris de Kruijff
    Date created: 02-Oct-17
"""

stations_list = ["Schagen", "Heerhugowaard", "Alkmaar", "Castricum", "Zaandam", "Amsterdam Sloterdijk", "Amsterdam Centraal",
            "Amsterdam Amstel", "Utrecht Centraal", "’server_socket-Hertogenbosch", "Eindhoven", "Weert", "Roermond", "Sittard",
            "Maastricht"]


def get_begin_station(stations):
    while True:
        try:
            user_input = str(input("Enter begin station: "))
            for station in stations:
                if station.lower() == user_input.lower():
                    return station
            print("This trsin does not pass {}. Please try again.".format(user_input))
            continue
        except ValueError:
            print("Invalid input, please try again.")
            continue


def get_end_station(stations, begin_station):
    while True:
        try:
            user_input = str(input("Enter end station: "))
            for station in stations:
                if station.lower() == user_input.lower():
                    if stations.index(station) != stations.index(begin_station):
                        return station
                    else:
                        print("Invalid input, please try again.")
            print("This train does not pass {}. Please try again.".format(user_input))
            continue
        except ValueError:
            print("Invalid input, please try again.")
            continue


def notify_journey(stations, begin_station, end_station):
    print("The begin station is number {} in it'server_socket journey".format(stations.index(begin_station) + 1))
    print("The end station is number {} in it'server_socket journey".format(stations.index(end_station) + 1))
    print("The distance is {} stations".format(abs(stations.index(end_station) - stations.index(begin_station))))
    print("You get on station : {}".format(begin_station))
    for station in stations:
        if stations.index(station) > stations.index(begin_station) and stations.index(station) < stations.index(end_station):
            print ('    - {}'.format(station))
    print("You get out on station : {}".format(end_station))


start = get_begin_station(stations_list)
end = get_end_station(stations_list, start)
notify_journey(stations_list, start, end)
