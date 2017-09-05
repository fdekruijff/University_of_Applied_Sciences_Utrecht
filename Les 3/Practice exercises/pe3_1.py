"""
    Title: Practice exercise 3_1
    Author: Floris de Kruijff
    Date created: 05-Sep-17
"""

while True:
    try:
        score = float(input("Geef je score: "))

        if score > 15:
            print("Met een score van " + str(score) + " ben je geslaagd!")
        else:
            print("Helaas is een score van " + str(score) + " niet voldoende om te slagen")
        exit(0)
    except ValueError:
        print("Voer een cijfer in.")
        continue

# Wat gebeurt er als je de tweede print()-opdracht niet recht onder de eerste zou plaatsen maar bijvoorbeeld
# recht onder de ‘i’ van het if-statement?
# De parser constateerd dan een indent error
