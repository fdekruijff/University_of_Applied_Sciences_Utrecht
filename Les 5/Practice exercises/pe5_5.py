"""
    Title: Practice exercise 5_5
    Author: Floris de Kruijff
    Date created: 14-Sep-17
"""


def average(string: str):
    string = string.split(' ')

    total_length = 0
    for word in string:
        total_length += len(word)

    return total_length / len(string)


print("The average length of each word is {}".format(average(input("Please enter a random sentence: "))))

