"""
    Title: Practise exercise 7_4
    Author: Floris de Kruijff
    Date created: 28-Sep-17
"""


def ticker(filename):
    """ Returns ticker symbol array from file """
    return_dict = {}
    with open(filename, 'r') as ticker_file:
        for line in ticker_file:
            line = line.split(':')
            return_dict[line[0]] = line[1]
        ticker_file.close()
    return return_dict


ticker_dict = ticker('ticker_symbol.txt')

while True:
    user_input = input("Enter company name: ")

    if user_input in ticker_dict:
        print("Ticker symbol: {}".format(ticker_dict[user_input]))
    else:
        print("This company is not found, please try again")
        continue

    user_input = input("Enter Ticker symbol: ")
    user_input = user_input + '\n'

    if user_input in ticker_dict.values():
        # Explanation for format() statement below, for myself.
        # 1. format() is called upon string to populate brackets in string.
        # 2. ticker_dict.keys() is converted to a list
        # 3. The index of the above created list is ticker_dict.values() converted to a list
        # 4. The above index of ticker_dict.values list is the user input
        print("Ticker symbol: {}".format(list(ticker_dict.keys())[list(ticker_dict.values()).index(user_input)]))
        break
    else:
        print("This company is not found, please try again")
        continue
