"""
    Title: Final Assignment 2
    Author: Floris de Kruijff
    Date created: 08-Sep-17
"""
import time


def standaardPrijs(afstandKM: int) -> float:
    if afstandKM <= 0:
        return 0
    elif afstandKM <= 50:
        return  (afstandKM * 0.8)
    else:
        return (afstandKM * 0.6) + 15


def ritPrijs(leeftijd: int, weekendRit: bool, afstandKM: int) -> float:
    standaard_prijs = standaardPrijs(afstandKM)

    vandaag = time.strftime("%A")

    if weekendRit:
        standaard_prijs *= 0.6
    elif (((vandaag == "Monday") or
             (vandaag == "Tuesday") or
             (vandaag == "Wednesday") or
             (vandaag == "Thursday") or
             (vandaag == "Friday")) and
            (leeftijd <= 12 or leeftijd >= 65)):
        standaard_prijs *= 0.7
    else:
        standaard_prijs *= 0.65

    return standaard_prijs


print(ritPrijs(50, False, 20))
