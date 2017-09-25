"""
    Title: Final Assignment 6
    Author: Floris de Kruijff
    Date created: 21-Sep-17
"""

import os

# lockers.csv data storage as follows > locker_number,in_use,pin_code

# Statically define total available lockers for display purposes.
locker_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
locker_file_name = 'locker.csv'


def initialise_locker_file(filename: str):
    """ This writes default values for the 12 available lockers """
    with open(filename, 'w') as file:
        for locker in locker_range:
            file.write('{},{},{}\n'.format(locker, 'Free', '0000'))
    file.close()


def write_file(filename: str, input_string):
    """ Generic function to write string to desired filename """
    # Check if the filename is found, if so return the file.
    try:
        with open(filename, 'w') as file:
            # Make sure the locker file is initialised properly.
            if os.path.getsize(filename) != 0:
                file.write(input_string)
            else:
                initialise_locker_file(filename)
                return write_file(filename, input_string)
    except FileNotFoundError:
        # If the file is not found it is created, the function is called again
        # and should operate normally.
        open(filename, 'w')
        initialise_locker_file(filename)
        return write_file(filename, input_string)


def query_file(filename: str, keyword, index: int):
    """ Returns the line on which the keyword is found """
    # Check if the filename is found, if so return the file.
    try:
        with open(filename, 'r') as file:
            # Make sure the locker file is initialised properly.
            if os.path.getsize(filename) != 0:
                line_number = 1
                for line in file:
                    line = line.split(',')
                    if int(line[index]) == int(keyword):
                        return line, line_number
                    line_number += 1
                return -1
            else:
                initialise_locker_file(filename)
                return query_file(filename, keyword, index)
    except FileNotFoundError:
        # If the file is not found it is created, the function is called again
        # and should operate normally.
        open(filename, 'w')
        initialise_locker_file(filename)
        return query_file(filename, keyword, index)


def print_menu_options():
    """ Prints out the menu to the console, returns the users menu decision """
    print("1. I want a new locker")
    print("2. I want to open my locker")
    print("3. I want to return my locker")
    print("4. I want to know how many lockers are available")
    print("5. Exit the application")

    # Use the generic input function to ask a question and define the expected data type.
    return get_user_input("Please enter the menu number to continue: ", int)


def get_user_input(message: str, data_type):
    """ Generic user input function. Returns user input and make sures data type is correct """
    # Ask for user input based on the parameter message.
    return_value = input(message)

    try:
        # Check if the user input data type is the same as the one defined in the parameter.
        return_value = data_type(return_value)
    except ValueError:
        # If the data type is not the same, notify the user and ask again.
        print("Input is invalid, please try again.")
        get_user_input(message, data_type)
    else:
        return return_value


def get_free_locker() -> tuple:
    """ Return the first free locker number """
    for number in range(len(locker_range)):
        line = query_file(locker_file_name, number, 0)

        if line != -1:
            if line[0][1] == 'Free':
                # Locker is not in use
                return line[0][0], line[1]

    # If reached here it would appear so that all lockers are occupied.
    return -1, -1


def update_locker(locker_number: int, in_use: bool, pin_code: int, line_number: int):
    """ Updates desired locker information """

    



def new_locker():
    # Loop through the available lockers and check if it's occupied or not.
    locker_number = get_free_locker()

    if locker_number != -1:
        # There is a locker available.
        pin_code = hash(str(get_user_input("Please enter your desired 4 digit code for your locker: ", int)))

        # Now that we have the locker number and pin code we need, let's update this information in the csv file.
        update_locker(locker_number[0], True, pin_code, locker_number[1])
    else:
        # All lockers are occupied.
        print("There are currently no lockers available, please try again later.")


def open_locker():
    pass


def return_locker():
    pass


def check_availability():
    pass


while True:
    user_input = print_menu_options()

    if user_input == 1:
        new_locker()
    elif user_input == 2:
        open_locker()
    elif user_input == 3:
        return_locker()
    elif user_input == 4:
        check_availability()
    else:
        exit(0)
