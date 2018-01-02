"""
    Title: Final Assignment 2
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""


def default_price(distance_km: int) -> float:
    """ Returns the train ticket price per kilometer """
    if distance_km <= 0:
        return 0
    elif distance_km <= 50:
        return distance_km * 0.8
    else:
        return ((distance_km - 50) * 0.6) + 15


def ride_price(age: int, weekend_ride: bool, distance_km: int) -> float:
    """ Calculates the train ticket price based on kilometer, age, weekday and distance """
    price = default_price(distance_km)

    if (age >= 12 or age <= 64) and weekend_ride:
        price *= 0.6
    elif age <= 12 or age >= 65:
        if weekend_ride:
            price *= 0.65
        else:
            price *= 0.7
    return float(format(price, '.2f'))


# age: 50, not weekend, 20km |0 Price should be 16.00
print("Price for 20km is: {}".format(ride_price(50, False, 20)))

# age: 50, weekend, 20km | Price should be 9,60
print("Price for 20km is: {}".format(ride_price(50, True, 20)))

# age: 10, not weekend, 20km | Price should be 11.20
print("Price for 20km is: {}".format(ride_price(10, False, 20)))
