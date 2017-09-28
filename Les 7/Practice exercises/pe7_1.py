"""
    Title: Practice exercise 7_1
    Author: Floris de Kruijff
    Date created: 28-Sep-17
"""

number_list = []
input_number = None

while True:
    try:
        input_number = int(input("Enter a number: "))
    except ValueError:
        continue

    if input_number != 0:
        number_list.append(input_number)
    else:
        print("There were {} numbers entered, the sum is {}".format(str(len(number_list)), str(sum(number_list))))
        exit(0)
