"""
    Title: Practice exercise 3_2
    Author: Floris de Kruijff
    Date created: 05-Sep-17
"""

while True:
    try:
        leeftijd = int(input("Geef je leeftijd: "))
        passpoort = str(input("Nederlands paspoort: "))

        if passpoort.lower() == 'ja' and (leeftijd >= 18):
            print("Gefeliciteerd, je mag stemmen!")
        elif passpoort.lower() == 'ja' and (leeftijd < 18):
            print("Je bent nog te jong om te stemmen.")
        elif passpoort.lower() == 'nee':
            print("Je hebt een Nederlands passpoort nodig om te stemmen.")

        exit(0)
    except ValueError:
        print("Incorrecte invoer, probeer opnieuw.")
        continue
