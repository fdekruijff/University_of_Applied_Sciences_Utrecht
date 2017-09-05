"""
    Title: Practice exercise 2_2
    Author: Floris de Kruijff
    Date created: 04-09-2017
"""

import math

cijferICOR = 6.0
cijferPROG = 8.0
cijferCSN = 7.5

totaal = cijferICOR + cijferPROG + cijferCSN

gemiddelde = math.floor(totaal / 3)
beloning = totaal * 30.0
overzicht = "Gemiddelde cijfer: " + str(gemiddelde) + "\n" + "Beloning: " + str(beloning) + " euro"

print(overzicht)

