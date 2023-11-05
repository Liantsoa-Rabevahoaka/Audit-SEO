import re
from collections import defaultdict
import csv
from html import unescape
from urllib.parse import urlparse
import requests

class Filtrage:
    @staticmethod
    def occurrence_mots(texte):
        mots = re.findall(r'\b\w+\b', texte.lower())
        occurrences = defaultdict(int)
        for mot in mots:
            occurrences[mot] += 1
        occurrences_triees = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
        return occurrences_triees

    @staticmethod
    def filtrer_mots_parasites(structure_donnees, mots_parasites):
        mots_filtres = [(mot, occ) for mot, occ in structure_donnees if mot not in mots_parasites]
        return mots_filtres

    @staticmethod
    def recuperer_mots_parasites(nom_fichier):
        mots_parasites = []
        with open(nom_fichier, newline='', encoding='utf-8') as fichier_csv:
            lecteur = csv.reader(fichier_csv)
            for ligne in lecteur:
                mots_parasites.extend(ligne)
        return mots_parasites

    @staticmethod
    def creer_fichier_parasites(nom_fichier, mots_parasites):
        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(mots_parasites)

    @staticmethod
    def supprimer_balises_html(texte_html):
        texte_sans_balises = re.sub('<[^<]+?>', '', texte_html)
        texte_sans_balises = unescape(texte_sans_balises)
        return texte_sans_balises

    @staticmethod
    def extraire_valeurs_attribut(texte_html, balise, attribut):
        pattern = fr'<{balise}\s[^>]*{attribut}\s*=\s*["\'](.*?)["\']'
        valeurs = re.findall(pattern, texte_html, re.IGNORECASE)
        return valeurs

    @staticmethod
    def extraire_nom_domaine(url):
        parsed_url = urlparse(url)
        nom_domaine = parsed_url.netloc
        return nom_domaine

    @staticmethod
    def separer_url_par_domaine(nom_domaine, liste_url):
        appartiennent_au_domaine = []
        n_appartiennent_pas_au_domaine = []

        for url in liste_url:
            parsed_url = urlparse(url)
            if nom_domaine in parsed_url.netloc:
                appartiennent_au_domaine.append(url)
            else:
                n_appartiennent_pas_au_domaine.append(url)

        return appartiennent_au_domaine, n_appartiennent_pas_au_domaine

    @staticmethod
    def recuperer_texte_de_page(url):
        reponse = requests.get(url)
        texte_page = reponse.text
        return texte_page
