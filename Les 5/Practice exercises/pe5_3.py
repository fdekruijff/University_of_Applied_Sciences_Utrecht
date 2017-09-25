"""
    Title: Practice exercise 5_3
    Author: Floris de Kruijff
    Date created: 14-Sep-17
"""

line_count = 0
card_number_dict = {}
highest_card_number = 0

with open('card_numbers.txt') as card_number_file:
    for line in card_number_file:
        line = line.replace(', ', ',').replace('\n', ',').split(',')
        line_count += 1
        card_number_dict[line[0]] = line_count

        if int(line[0]) > int(highest_card_number):
            highest_card_number = line[0]

card_number_file.close()

print("This file has {} lines.".format(line_count))
print("The highest card number is: {}. It is on line {}".format(
    highest_card_number, card_number_dict[highest_card_number])
)
