"""
    Title: Practice exercises 6_2
    Author: Floris de Kruijff
    Date created: 21-Sep-17
"""

input_string = []
try:
    input_string = eval(input("Enter a list with a minimum of 10 strings: "))
except NameError:
    print("Input is not valid")
    exit(0)

new_list = []
for string in input_string:
    if len(string) == 4:
        new_list.append(string)

print("The new list with four-letter strings is: ", new_list)
