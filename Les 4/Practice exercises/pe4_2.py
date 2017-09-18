"""
    Title: Practice exercise 4_2
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""


def som(digit_list: list) -> int:
    """ Returns the som of the passed list"""
    return_value = 0
    for digit in digit_list:
        return_value += digit

    return return_value


print(som([4, 1, 6, 3, 7, 3]))
