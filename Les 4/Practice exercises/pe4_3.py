"""
    Title: Practice exercise 4_3
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""


def tall_enough(length: int) -> str:
    """
    :param length: Specify length
    :type length: int
    :return: Returns if you are tall enough or not.
    :rtype: str
    """
    if length >= 120:
        return "Je bent lang genoeg voor de attractie!"
    else:
        return "Sorry, je bent te klein!"