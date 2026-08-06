from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import csv


class Calendrier_FFVB(object):
    """
    Génération de calendrier (fichier .ics) pour des rencontres FFVB
    """
    def __init__(self, alerte = False):
        self.calendrier = Calendar()
        self.calendrier.add('prodid', '-//FFVB CAL//FR')
        self.calendrier.add('version', '2.0')
        self.alerte = alerte

    def ajout_match(self, date = '', heure = '', equipe_A = '', equipe_B = '', salle = '', journee ='', code_match = '', alerte = False):
        """
        Ajout d'une rencontre dans le calendrier
        On définit la durée d'une rencontre à 2H

        WARNNG : Les alertes ne fonctionent pas pour l'instant
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
            alarm.add('description', 'Match dans 30 minutes')
            event.add_component(alarm)
        self.calendrier.add_component(event)


    def creation_fichier(self, equipe = 'equipe'):
        """
        Création du fichier .ics
        """
        if self.alerte :
            nom_fichier = '%s_alerte.ics' % (equipe)
        else:
            nom_fichier = '%s.ics' % (equipe)
        with open(nom_fichier, 'wb') as f:
            f.write(self.calendrier.to_ical())

class CSV_FFVB(object):
    """
    Lit le fichier CSV généré sur le site de la FFVB

    Sous forme d'un dictionnaire avec les éléments suivant :
        Entité  Code région
        Jo      Numéro de la journée
        Match   Code du match
        Date    date (YYYY-MM-DD)
        Heure   heure (HH:MM)
        EQA_no  Numéro unique de l'équipe A
        EQA_nom Nom de l'équipe A
        EQB_no  Numéroe unique de l'équipe B
        EQB_nom Nom de l'équipe B
        Set     résultat en set (x/x)
        Score   score des set (xx-xx,xx-xx,)
        Total   total des points (xx-xx)
        Salle   Gymnase
        Arb1    Nom arbitre 1
        Arb2    Nom arbitre 2


    """
    def __init__(self, fichier):
        self.fichier = fichier
        self.donne= []
        self.__parse__()

    def __parse__(self):
        """
        Parse le fichier
        """
        with open(self.fichier, mode = 'r', newline='') as fichier:
            ligne = csv.DictReader(fichier, delimiter=';')
            for l in ligne :
                self.donne.append(l)

    def liste_match(self, equipe):
        """
        Créé une liste des matchs pour une équipe
        """
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
    liste_match = fichier.liste_match('FLAVIGNY')

    cal = Calendrier_FFVB()
    for match in liste_match :
        cal.ajout_match(match['Date'], match['Heure'], match['EQA_nom'], match['EQB_nom'], match['Salle'], match['Jo'], match['Match'])
    #cal.ajout_match('06/08/2026', '17:00', 'FLAVIGNY', 'BAM1', "GYMNASE DU JEUX", '1', 'OP1A001')
    cal.creation_fichier()
    pass

