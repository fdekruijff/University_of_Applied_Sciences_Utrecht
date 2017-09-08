"""
    Title: Practice exercise 3_6
    Author: Floris de Kruijff
    Date created: 05-Sep-17
"""

s = "Guido van Rossum heeft programmeertaal Python bedacht."

for letter in s:
    if (str(letter).lower() == 'a' or
        str(letter).lower() == 'e' or
        str(letter).lower() == 'i' or
        str(letter).lower() == 'o' or
            str(letter).lower() == 'u'):
        print(letter)
