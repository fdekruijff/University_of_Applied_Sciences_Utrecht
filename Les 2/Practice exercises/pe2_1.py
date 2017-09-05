"""
    Title: Practice exercise 2_1
    Author: Floris de Kruijff
    Date created: 04-09-2017
"""

letters = ('X', 'C', 'X', 'B', 'C', 'C', 'C', 'C', 'D')

letterArray = list(letters)
letterArray.sort()

previousLetter = ''
for letter in letterArray:
    if letter != previousLetter:
        print(letter + ': ' + str(letterArray.count(letter)))

    previousLetter = letter
