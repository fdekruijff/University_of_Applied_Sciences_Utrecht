"""
    Title: Practice exercise 4_6
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""

letters = ['a', 'b', 'c']


def modify(letters: list):
    nonlocal letters
    letters = ['d', 'e', 'f']


print(letters)
modify(letters)
print(letters)
