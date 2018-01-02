"""
    Title: Practise exercise 7_5
    Author: Floris de Kruijff
    Date created: 28-Sep-17
"""


def names():
    names_list = []
    while True:
        try:
            user_input = str(input("Next name: "))

            if user_input == '':
                return names_list
            else:
                names_list.append(user_input)
        except TypeError:
            continue


name_list = names()

while name_list:
    for name in name_list:
        counter = 0
        while name in name_list:
            counter += 1
            name_list.remove(name)

        if counter == 1:
            print("There is 1 student by the name of {}".format(name))
        else:
            print("There are {} students by the name of {}".format(counter, name))
