"""
    Title: Practice exercise 3_2
    Author: Floris de Kruijff
    Date created: 05-Sep-17
"""

while True:
    try:
        leeftijd = float(input("Geef je leeftijd: "))
        passpoort = str(input("Nederlands paspoort: "))

        if passpoort.lower() == 'ja' or passpoort.lower() == 'nee':
            if leeftijd >= 18 and passpoort.lower() == 'ja':
                print("Gefeliciteerd, je mag stemmen!")
            elif leeftijd < 18:
                print("Je bent nog te jong om te stemmen.")
            else:
                print("Je hebt een Nederlands passpoort nodig om te stemmen.")
        else:
            print("Geef 'Ja' of 'Nee' aan of u in bezit bent van een Nederlands paspoort.")
            continue

        exit(0)
    except ValueError:
        print("Voer een cijfer in.")
        continue
