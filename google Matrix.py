import googlemaps


def distance(origin, destination):
    google_maps = googlemaps.Client(key='AIzaSyB3sE6Ekts-GoPlZ8vJ8P8i0UL1rVFnnPI')
    delta = google_maps.distance_matrix(origin, destination)['rows'][0]['elements'][0]['distance']['text']
    return delta

kaartautomaat=52.3702157,4.895167899999933

kleinsteafstand = 10**10
monteurs= {'tim':[52.1561113,5.387826600000039], 'jan':[52.09073739999999,5.121420100000023], 'dick':[51.9244201,4.4777325999999675]}


for Name, GEO in monteurs.items():
        geo= (tuple(GEO))
        afstand= (distance(geo, kaartautomaat))
        afstand= afstand[:-2]
        afstand= float(afstand)


        if afstand <= kleinsteafstand:
            kleinsteafstand = afstand
            kleinsteafstandmonteur = Name

print (kleinsteafstandmonteur)




