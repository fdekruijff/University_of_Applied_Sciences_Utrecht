"""
    Title: Practice exercise 4_6
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""

letters = ['a', 'b', 'c']


def modify(old_letters: list):
    old_letters.clear()
    new_letters = ['d', 'e', 'f']

    global letters
    letters = new_letters


def modify_improved():
    return ['d', 'e', 'f']


print(letters)
modify(letters)
letters = modify_improved()
print(letters)


# Je kan niet zo maar letters = list() doen omdat letters in de buitenste scope zit.
# Op de manier waar ik het doe zou het ook werken met een String.
# Globals gebruiken is bad-practice, het is beter om return statements te gebruiken
# Een String object is inmutable. Een list kan gewijzigd worden.
