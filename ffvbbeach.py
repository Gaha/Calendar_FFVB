import requests
from html.parser import HTMLParser

"""
Récupération de la page HTML du tableau des résultats 

saison : année de la saison
codent : code de la région
poule : code de la poule

URL générale (pour connaitre les poules : https://www.ffvbbeach.org/ffvbapp/resu/vbspo_home.php?saison=2019%2F2020&codent=PTLO54)


"""

class ffvbbeach(object):
    """
    Analyse la page des résultats
    """
    def __init__(self):
        self.url = 'https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier.php'
        self.url_export = 'https://www.ffvbbeach.org/ffvbapp/resu/vbspo_calendrier_export.php'

    def fichier_csv(self, saison, code, poule):
        """
        Export au format csv
        """
        payload = {
            'cal_saison' : saison,
            'cal_codent' : code,
            'cal_codpoule' : poule,
            'cal_coddiv' : '',
            'cal_codtour' : '',
            'typ_edition' : 'E' ,
            'type' : 'RES' ,
            'rech_equipe' : ''
        }
        print(payload)
        r = requests.post(self.url_export, data=payload, verify=False, stream=True)

        if r.status_code == 200:
            print('Successful request!')

        nom_fichier = '%s_%s_%s.csv' % (code, poule, saison.replace('/','-'))
        with open(nom_fichier, 'wb') as out_file:
            out_file.write(r.content)
      

    def fichier_pdf(self):
        pass

    def fichier_html(self):
        payload = {'saison' : '2025/2026', 'codent' : 'PTLO54', 'poule' : 'OP1'}
        r = requests.get(url, params=payload, verify=False)
        pass

   
if __name__ == "__main__":
    ffvb = ffvbbeach()
    ffvb.fichier_csv('2025/2026','PTLO54', 'OP1')
