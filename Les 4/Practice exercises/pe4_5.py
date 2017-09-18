"""
    Title: Practice exercise 4_5
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""


def square_sum(numbers: list) -> int:
    """ Returns the square root sum of all positive integers """
    return_value = 0
    for number in numbers:
        if type(number) == int:
            if number >= 0:
                return_value += number**2
        else:
            print("List is not made up entirely of Integer types.")
            return -1

    return return_value


print(square_sum([2, -4, 3, 5, -7, 9]))
