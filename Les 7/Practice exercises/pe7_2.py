"""
    Title: Practice exercise 7_2
    Author: Floris de Kruijff
    Date created: 28-Sep-17
"""

while True:
    try:
        input_string = str(input("Enter a four letter word: "))
    except ValueError:
        print("This is not a word, try again.")
        continue

    if len(input_string) == 4:
        exit()
