"""
    Title: Practice exercise 5_4
    Author: Floris de Kruijff
    Date created: 14-Sep-17
"""

import datetime

with open('runners.txt', 'w') as runners_file:
    while True:
        try:
            print("Type 'exit' to exit the application")
            runner_name = str(input("Runners name: "))

            if runner_name.lower() == 'exit':
                exit(0)

            runner_time = str(input("Finish time: (10:45:52) "))

            today = datetime.datetime.today()

            runners_file.write("{}, {}, {}\n".format(today.strftime("%a %d %b %Y"), runner_time, runner_name))
            print("Enter another runners name.")

        except ValueError:
            print("Input is invalid, please try again.")
            continue
