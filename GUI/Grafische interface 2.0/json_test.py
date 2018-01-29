import csv
import datetime


def get_time():
    """ Returns current time in format %d-%m-%Y %X """
    return datetime.datetime.now().strftime('%d-%m-%Y %X')

plot_x = []
plot_y = []
bestand_locatie = 'waterpeil.csv'

with open(bestand_locatie, 'r') as myCSVFILE:  # Leest het geschreven csv bestand
    reader = csv.reader(myCSVFILE, delimiter=';')
    index = 2
    myCSVFILE.readline()

    for lijn in reader:  # Elke lijn met waardes komt in een tuple
        datum = lijn[0][-5:]
        waterstand = lijn[2]
        if len(waterstand) != 0:
            plot_x.append(datum)
            plot_y.append(waterstand)# Sla de laatste ingevulde waarde van de waterstand op

print(get_time())
print(plot_x[-6:])
print(plot_y[-6:])
        #if len(waterstand) != 0:
        #    laatste_waterstand = waterstand  # Sla de laatste ingevulde waarde van de waterstand op