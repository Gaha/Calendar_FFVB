import requests
from html.parser import HTMLParser

"""
Récupération de la page HTML du tableau des résultats 

saison : année de la saison
codent : code de la région
poule : code de la poule

URL générale (pour connaitre les poules : https://www.ffvbbeach.org/ffvbapp/resu/vbspo_home.php?saison=2019%2F2020&codent=PTLO54)


"""

payload = {'saison' : '2025/2026', 'codent' : 'PTLO54', 'poule' : 'OP1'}
url = 'https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php'

r = requests.get(url, params=payload, verify=False)

print(r.text)
