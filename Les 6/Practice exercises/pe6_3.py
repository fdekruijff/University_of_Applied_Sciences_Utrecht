"""
    Title: Practice exercise 6_3
    Author: Floris de Kruijff
    Date created: 21-Sep-17
"""

input_list = "5-9-7-1-7-8-3-2-4-8-7-9"

input_list = input_list.split('-')
input_list.sort()

# Convert the string objects to an integer object
for x in input_list:
    input_list[input_list.index(x)] = int(x)

print("Sorted list of integers: ", input_list)
print("Largest number: {} and Smallest number: {}".format(str(max(input_list)), str(min(input_list))))
print("Number of integers: {} and their sum: {}".format(str(len(input_list)), str(sum(input_list))))
print("Average: {0:.2f}".format(float(int(sum(input_list)) / len(input_list))))
