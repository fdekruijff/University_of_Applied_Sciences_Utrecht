"""
    Title: Practice exercise 5_1
    Author: Floris de Kruijff
    Date created: 14-Sep-17
"""


def convert(celsius: float) -> float:
    """ Returns Celsius converted to Fahrenheit """
    return (celsius * 1.8) + 32


def table():
    """ Prints out table for -30 to 40 degrees Celsius """

    for x in range(-30, 41):
        print("{} degrees Celsius is {} Fahrenheit".format(x, convert(x)))


table()
