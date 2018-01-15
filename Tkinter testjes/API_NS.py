#Studentnummer: 1644744
#Naam: Remco Taal
import requests, xmltodict

vertrekTijd = ''
treinSoort = ''
station = ''


def request():
    'Stuurt een request naar de server van NS en returnt een XML'
    global station
    station = input('Vul het station in: ')
    auth_details = ('remcotaal@hotmail.com', 'Euclf-6uz8iWdUOl7LpERmknqv4u5IEY1Wr3hC2pkK3rJQnum3aNLg')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + station
    response = requests.get(api_url, auth=auth_details)
    return response.text

dictionary = xmltodict.parse(request())

if 'error' not in dictionary:           #De XML bevat een dictionary error wanneer een verkeerde waarde wordt ingevuld

    for tijd in dictionary['ActueleVertrekTijden']['VertrekkendeTrein']:
        vertrekTijd = tijd['VertrekTijd']
        vertrekTijd = vertrekTijd[11:19]
        treinSoort = tijd['TreinSoort']
        eindbestemming = tijd['EindBestemming']
        spoor = tijd['VertrekSpoor']['#text']
        #print('Het begin station is: {} {:9} {} uur De eindbestemming is: {}'.format(station.capitalize(), treinSoort, vertrekTijd, eindbestemming))
        print('U reist vanaf station {} de trein komt om {} de eindbestemming is {}'.format(station, vertrekTijd, eindbestemming))

else:
    print(dictionary['error']['message'])
    request()





