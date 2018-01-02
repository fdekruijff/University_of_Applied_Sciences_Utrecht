"""
    Title: Final Assignment 6
    Author: Floris de Kruijff
    Date created: 27-Sep-17
"""

import os
import hashlib

# lockers.csv data storage as follows > locker_number,in_use,pin_code

# Statically define total available lockers for display purposes.
locker_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
locker_file_name = 'locker.csv'

# Define user feedback messages.
message1 = "Thank you for using this service."
message2 = "\nLocker {} has been reserved, thank you for using this service.\n"
message3 = "\nLocker {} has been opened.\nYour access to locker {} has been revoked.\n"
message4 = "\nLocker {} has been opened.\n"
message5 = "\nThis locker is currently not in use, please try a different locker.\n"
message6 = "\nThere is 1 locker available.\n"
message7 = "\nThere are {} lockers available.\n"

menu = "1. I want a new locker\n" \
       "2. I want to open my locker\n" \
       "3. I want to return my locker\n" \
       "4. I want to know how many lockers are available\n" \
       "5. Exit the application"

question1 = "Please enter the menu number to continue: "
question2 = "Please enter your desired 4 digit code for your locker: "
question3 = "Please enter your digit code: "
question4 = "Please enter your locker number (0 to exit): "

error1 = "\nInput is invalid, please try again.\n"
error2 = "\nYour pin code is not sufficiently long. Please try again.\n"
error3 = "\nThere are currently no lockers available, please try again later.\n"
error4 = "\nThis pin code is incorrect, please try again.\n"


def initialise_locker_file(filename: str):
    """ This writes default values for the predefined amount of available lockers """
    with open(filename, 'w') as file:
        for locker in locker_range:
            file.write('{},{},{}\n'.format(locker, 'Free', '0000'))
    file.close()


def is_file_present(filename):
    """ Generic function used to check whether file is present in file system or not """
    if not os.path.exists(filename):
        # If it is not present, create it and initialise it.
        open(filename, 'w')
        initialise_locker_file(filename)
        return False
    return True


def write_file(filename: str, input_string, truncate: bool):
    """ Generic function to write string to desired filename """
    # Check if the filename is found, append input string, or rewrite completely based on truncate boolean.
    if is_file_present(filename):
        with open(filename, 'w') as file:
            if truncate:
                # Truncate file and reinitialise default values.
                file.truncate()
                initialise_locker_file(locker_file_name)

            # Make sure the locker file is initialised properly. If file size is 0 something is wrong.
            if os.path.getsize(filename) != 0:
                # Write values to file.
                file.write(input_string)
            else:
                # Something is off, reinitialise file and recursively recall function to try again.
                initialise_locker_file(filename)
                return write_file(filename, input_string, truncate)
    else:
        return write_file(filename, input_string, truncate)


def query_entire_file(filename: str):
    """ Returns entire file as list, split by line breaks """
    # Check if the filename is found, if so return the file.
    if is_file_present(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            file.close()
            return lines
    else:
        return query_entire_file(filename)


def query_file(filename: str, keyword, index: int):
    """ Returns the line on which the keyword is found """
    # Check if the filename is found, if so return the file.
    if is_file_present(filename):
        with open(filename, 'r') as file:
            # Make sure the locker file is initialised properly.
            if os.path.getsize(filename) != 0:
                line_number = 0
                for line in file:
                    line = line.split(',')
                    if int(line[index]) == int(keyword):
                        return line, line_number
                    line_number += 1
                return None
            else:
                initialise_locker_file(filename)
                return query_file(filename, keyword, index)
    else:
        return query_file(filename, keyword, index)


def print_menu_options():
    """ Prints out the menu to the console, returns the users menu decision """
    print(menu)

    # Use the generic input function to ask a question and define the expected data type.
    return get_user_input(question1, int)


def get_user_input(message: str, data_type):
    """ Generic user input function. Returns user input and make sures data type is correct """
    # Ask for user input based on the parameter message.
    return_value = input(message)

    try:
        # Check if the user input data type is the same as the one defined in the parameter.
        return_value = data_type(return_value)
    except ValueError:
        # If the data type is not the same, notify the user and ask again.
        print(error1)
        get_user_input(message, data_type)
    else:
        return return_value


def get_free_locker():
    """ Return the first free locker number """
    for number in range(len(locker_range) + 1):
        # Call the generic query function to check if this locker number is available.
        # Locker number resides in index number 0.
        line = query_file(locker_file_name, number, 0)

        # If the locker number has been found, check if the status is 'Free'. The way I designed this this information
        # is stored in element 1 of list 0 in the line variable.
        if line:
            if line[0][1] == 'Free':
                # Locker is not in use
                return line[0][0], line[1]

    # If reached here it would appear so that all lockers are occupied. Return None for easy if logic later on.
    return None


def update_locker(locker_number: int, in_use: str, pin_code: str, line_number: int):
    """ Updates desired locker information """
    # We retrieve the entire file.
    current_file = query_entire_file(locker_file_name)
    # Next we update the desired line_number with the passed parameters.
    current_file[line_number] = '{},{},{}\n'.format(locker_number, in_use, pin_code)

    # After that we convert the list back to a String to be written back to the database
    output = ''
    for line in current_file:
        output += line

    # Call the generic function to rewrite the database, Truncate is True.
    write_file(locker_file_name, output, True)


def new_locker():
    """ Finds available locker and updates database with information """
    # Loop through the available lockers and check if it'server_socket occupied or not.
    locker_number = get_free_locker()

    if locker_number:
        # There is a locker available, request a desired pin code and hash it with SHA256.
        pin_code = str(get_user_input(question2, int))

        # Make sure the entered pin code is at least four digits long.
        if len(pin_code) < 4:
            print(error2)
            new_locker()
        else:
            pin_code = hashlib.sha256(pin_code.encode('utf-8')).hexdigest()

            # Now that we have a free locker number, a pin code, and the line number. We call update_locker() to pass
            # this information to the database file.
            update_locker(int(locker_number[0]), 'In Use', pin_code, locker_number[1])
            print(message2.format(locker_number[0]))
    else:
        # Unfortunately all lockers are currently in use, nothing we can do here.
        print(error3)


def access_locker(file_code: str) -> bool:
    """ A generic function to gain access to a locker """
    # Request users pin_code, hash it to SHA256 instantly for security purposes.
    pin_code = hashlib.sha256(
        str(get_user_input(question3, int)).encode('utf-8')
    ).hexdigest()

    # If the two hashes match the pin code is correct, return True. If not False will be returned.
    if str(pin_code) == file_code:
        return True
    return False


def open_locker(return_locker: bool):
    """ Handles the opening and returning of a locker """
    # Request the users locker number.
    locker_number = get_user_input(question4, int)

    # Give user the option to back to main menu
    if not locker_number:
        print()
        return

    # Find the locker number in the file with query_file().
    line = query_file(locker_file_name, locker_number, 0)

    # None will be returned if the parameter locker_number is not found.
    if line:
        # Make sure this locker is 'In Use'.
        if str(line[0][1]) == 'In Use':
            # Check if user has access, remove line breaks while we're at it.
            if access_locker(str(line[0][2]).replace('\n', '')):
                if return_locker:
                    # Now that the locker is open, remove information from the file to make it available again.
                    update_locker(locker_number, 'Free', '0000', line[1])
                    print(message3.format(locker_number, locker_number))
                else:
                    # If return_locker is False, just notify that the locker is now open.
                    print(message4.format(locker_number))
            else:
                # The pin code was not correct, notify and recursively recall this function to alarm_running over.
                print(error4)
                open_locker(return_locker)
        else:
            # The locker is not in use, notify and recursively recall this function to alarm_running over.
            print(message5)
            open_locker(return_locker)


def check_availability():
    """ Checks the amount of free lockers """
    free_locker_list = []

    # Loop through all lockers in database.
    for locker_number in locker_range:
        line = query_file(locker_file_name, locker_number, 0)

        if line:
            # If the locker is 'Free', append it to the list.
            if str(line[0][1]) == 'Free':
                free_locker_list.append(locker_number)

    if len(free_locker_list) != 0:
        if len(free_locker_list) == 1:
            print(message6)
        else:
            print(message7.format(len(free_locker_list)))
    else:
        print(error3)


if __name__ == '__main__':
    while True:
        user_input = print_menu_options()

        if user_input == 1:
            new_locker()
        elif user_input == 2:
            open_locker(return_locker=False)
        elif user_input == 3:
            open_locker(return_locker=True)
        elif user_input == 4:
            check_availability()
        else:
            exit(message1)
