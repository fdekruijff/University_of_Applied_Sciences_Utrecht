"""
    Title: Practice exercise 6_1
    Author: Floris de Kruijff
    Date created: 21-Sep-17
"""


def seasons(month: int) -> str:
    """ Returns season based on month number """
    if 3 <= month <= 5:
        return "Spring"
    elif 6 <= month <= 8:
        return "Summer"
    elif 9 <= month <= 11:
        return "Fall"
    elif 12 <= month <= 2:
        return "Winter"


print(seasons(4))
