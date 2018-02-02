import csv
import requests

CSV_URL = 'https://waterberichtgeving.rws.nl/wbviewer/maak_grafiek.php?loc=HOEK&set=eindverwachting&nummer=1&format=csv'
bestandLocatie = 'Waterpeil.csv'


def haal_gegevens_op():
    "Haalt gegevens op en schrijft dit weg in een csv bestand"
    with requests.Session() as s:   #Haalt gegevens op van de server
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        lezen = csv.reader(decoded_content.splitlines(), delimiter=';')
        lijst = list(lezen)


    with open(bestandLocatie, 'w', newline='') as myCSVFile:    #Schrijft gegevens weg in csv bestand
        schrijven = csv.writer(myCSVFile, delimiter=';')

        for lijn in lijst:
            schrijven.writerow(lijn)


with open(bestandLocatie, 'r') as myCSVFILE:                #Leest het geschreven csv bestand
    reader = csv.reader(myCSVFILE, delimiter=';')
    myCSVFILE.readline() #Slaat de eerste regel over

    for lijn in reader:  # Elke lijn met waardes komt in een tuple
        opzet = int(lijn[3])  # Zet de waarde om naar een integer
        if opzet > 100:  # Als de verwachte opzet te hoog is wordt dit geprint
            print('De verwachte opzet waarde {} is te hoog'.format(opzet))