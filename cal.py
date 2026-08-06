from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import csv


class Calendrier_FFVB(object):
    """
    Génération de calendrier pour une équipe FFVB
    """
    def __init__(self, alerte = False):
        self.calendrier = Calendar()
        self.calendrier.add('prodid', '-//FFVB CAL//FR')
        self.calendrier.add('version', '2.0')
        self.alerte = alerte

    def ajout_match(self, date = '', heure = '', equipe_A = '', equipe_B = '', salle = '', journee ='', code_match = '', alerte = False):
        """
        journee : numero de ma journée, ex: 1
        code_match : ex : OP1A001
        Date: sous la forme JJ/MM/YYY
        heure : sous la forme HH:MM
        equipe_A
        equipe B
        salle
        alerte : si on souhaite ajouter une alerte

        titre : Match EQUIPE1 / EQUIPE2
        """

        titre = 'Match 🏐 %s / %s' % (equipe_A, equipe_B)
        gymnase = salle
        description = "Journéé %s\nCode du match : %s" % (journee, code_match)
        m_date = date.split('-')
        m_heure = heure.split(':')

        event = Event()
        event.add('summary', titre)
        event.add('dtstart', datetime(int(m_date[0]), int(m_date[1]), int(m_date[2]), int(m_heure[0]), int(m_heure[1]), 0))
        event.add('dtend', datetime(int(m_date[0]), int(m_date[1]), int(m_date[2]), int(m_heure[0]) + 2, int(m_heure[1]), 0))
        event.add('location', gymnase)
        event.add('description', description)

        if alerte or self.alerte:
            alarm = Alarm()
            alarm.add('action', 'DISPLAY')
            alarm.add('trigger', timedelta(minutes=-30))
            alarm.add('description', 'match dans 30 minutes')
            event.add_component(alarm)
        self.calendrier.add_component(event)


    def creation_fichier(self, equipe = 'equipe'):
        if self.alerte :
            nom_fichier = '%s_alerte.ics' % (equipe)
        else:
            nom_fichier = '%s.ics' % (equipe)
        with open(nom_fichier, 'wb') as f:
            f.write(self.calendrier.to_ical())

class CSV_FFVB(object):
    def __init__(self, fichier):
        self.fichier = fichier
        self.donne= []

    def parse(self):
        with open(self.fichier, mode = 'r', newline='') as fichier:
            ligne = csv.DictReader(fichier, delimiter=';')
            for l in ligne :
                self.donne.append(l)
    def liste_match(self, equipe):
        liste_match = []
        for match in self.donne:
            if match['EQA_nom'] == equipe or match ['EQB_nom'] == equipe :
                liste_match.append(match)
        return liste_match

class Equipe_FFVB(object):
    def __init__(self, nom, num_equipe = ''):
        self.nom_equipe = nom
        self.num_equipe = num_equipe

    def parse(self, fichier):
        """
        Parse le fichier csv
        """
        pass

    def calendrier(self):
        """
        cree le calendrier de l'équipe
        """
        pass


if __name__ == "__main__":
    fichier = CSV_FFVB("ffvb_calendrier.csv")
    fichier.parse()
    liste_match = fichier.liste_match('FLAVIGNY')

    cal = Calendrier_FFVB()
    for match in liste_match :
        cal.ajout_match(match['Date'], match['Heure'], match['EQA_nom'], match['EQB_nom'], match['Salle'], match['Jo'], match['Match'])
    #cal.ajout_match('06/08/2026', '17:00', 'FLAVIGNY', 'BAM1', "GYMNASE DU JEUX", '1', 'OP1A001')
    cal.creation_fichier()
    pass

