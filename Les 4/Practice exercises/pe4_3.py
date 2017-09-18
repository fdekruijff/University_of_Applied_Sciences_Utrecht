"""
    Title: Practice exercise 4_3
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""


def tall_enough(length: int) -> str:
    """ Returns whether your length is tall enough  or not """
    if length >= 120:
        return "Je bent lang genoeg voor de attractie!"
    else:
        return "Sorry, je bent te klein!"


print(tall_enough(150))
