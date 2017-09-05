"""
    Title: Practice exercise 2_4
    Author: Floris de Kruijff
    Date created: 04-09-2017
"""

while True:
    try:
        uurLoon = float(input("Wat verdien je per uur: "))

        while True:
            try:
                uurGewerkt = int(input("Hoeveel uur heb je gewerkt: "))

                print(str(uurGewerkt) + " uur gewerkt lever " + str(uurLoon * uurGewerkt) + " Euro op.")
                exit(0)
            except ValueError:
                print("Voer een cijfer in.")
                continue
    except ValueError:
        print("Voer een cijfer in.")
        continue
