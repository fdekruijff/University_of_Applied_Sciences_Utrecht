"""
    Title: Practise exercise 5_2
    Author: Floris de Kruijff
    Date created: 14-Sep-17
"""

with open('card_numbers.txt') as card_number_file:
    for line in card_number_file:
        line = line.replace(', ', ',').replace('\n', ',').split(',')

        print("{} has card number: {}".format(line[1], line[0]))

card_number_file.close()
