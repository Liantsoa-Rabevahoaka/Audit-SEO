import tkinter as tk
from tkinter import Menu, messagebox
from AuditSEO.Begin.filtrage import Filtrage
import re
from urllib.parse import urlparse
import csv


class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        master.title("SeEyOu")
        master.minsize(1000, 600)

       # self.canvas = tk.Canvas(master)
        #self.canvas.pack(fill=tk.BOTH, expand=True)

        #scroll_bar = Scrollbar(master, orient="vertical", command=self.canvas.yview)
        #scroll_bar.pack(side="right", fill="y")

        #self.canvas.configure(yscrollcommand=scroll_bar.set)

        #self.scrollbar_vertical = tk.Scrollbar(master, command=self.canvas.yview)
        #self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        #self.canvas.configure(yscrollcommand=self.scrollbar_vertical.set)

        #self.frame = tk.Frame(self.canvas)
        #self.canvas.create_window((0, 0), window=self.frame, anchor="nw")


        self.menubar = Menu(master)
        master.config(menu=self.menubar)

        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Créer", command=self.alert)
        menu1.add_command(label="Editer", command=self.alert)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=master.quit)
        self.menubar.add_cascade(label="Fichier", menu=menu1)

        menu2 = Menu(self.menubar, tearoff=0)
        menu2.add_command(label="Couper", command=self.alert)
        menu2.add_command(label="Copier", command=self.alert)
        menu2.add_command(label="Coller", command=self.alert)
        self.menubar.add_cascade(label="Editer", menu=menu2)

        menu3 = Menu(self.menubar, tearoff=0)
        menu3.add_command(label="A propos", command=self.alert)
        self.menubar.add_cascade(label="Aide", menu=menu3)

        self.frame_rechercher = tk.Frame(master)
        self.frame_rechercher.pack(anchor='w', padx=10, pady=5)

        self.label_url = tk.Label(self.frame_rechercher, text="URL : ")
        self.label_url.pack(side=tk.LEFT)

        self.rechercher = tk.Entry(self.frame_rechercher, width=50)
        self.rechercher.pack(side=tk.LEFT)

        self.label_mots_parasites = tk.Label(master, text="Mots Parasites (séparés par des virgules) : ")
        self.label_mots_parasites.pack()

        self.mots_parasites_entry = tk.Entry(master, width=50)
        self.mots_parasites_entry.pack()

        self.label_mots_recherches = tk.Label(master, text="Mots à rechercher (séparés par des virgules) : ")
        self.label_mots_recherches.pack()

        self.mots_recherches_entry = tk.Entry(master, width=50)
        self.mots_recherches_entry.pack()

        self.analyser = tk.Button(master, text="ANALYSER", command=self.executer_audit)
        self.analyser.pack(padx=5)

        self.resultats_label = tk.Label(master, text="TEXTE RECUPERER")
        self.resultats_label.pack(pady=10)

        self.texte_recupere = tk.Text(master, height=5, width=100)
        self.texte_recupere.pack()

    def alert(self):
        messagebox.showinfo("Alerte", "Fonction non implémentée.")

    def executer_audit(self):
        url_page_audite = self.rechercher.get()
        mots_parasites = self.mots_parasites_entry.get().split(",")
        mots_recherches = self.mots_recherches_entry.get().split(",")
        filtrage = Filtrage()

        # Récupération du texte de la page
        texte_page = filtrage.recuperer_texte_de_page(url_page_audite)

        # Récupération du texte de la page et suppression des balises HTML
        texte_nettoye = filtrage.supprimer_balises_html(texte_page)

        # Écriture des mots parasites dans un fichier CSV
        with open('parasite.csv', mode='w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(mots_parasites)

        # Extraction des mots clés et de leurs occurrences
        structure_donnees = Filtrage.occurrence_mots(texte_page)
        mots_cles = "\nMots clés avec leurs occurrences :\n"
        for mot, occurrence in structure_donnees[:3]:
            mots_cles += f"{mot} : {occurrence}\n"

        # Extraction des liens entrants et sortants
        liens = re.findall(r'href=[\'"]?([^\'" >]+)', texte_page)
        nb_liens_entrants = sum(urlparse(url).netloc == urlparse(url_page_audite).netloc for url in liens)
        nb_liens_sortants = len(liens) - nb_liens_entrants
        infos_liens = f"\nNombre de liens entrants : {nb_liens_entrants}\nNombre de liens sortants : {nb_liens_sortants}\n"

        # Recherche de mots spécifiques sur le site
        occurrences_mots_recherches = {}
        for mot in mots_recherches:
            occurrences_mots_recherches[mot] = structure_donnees[mot] if mot in structure_donnees else 0

        # Afficher les occurrences des mots recherchés
        occurences_affichage = "\nOccurrences des mots recherchés :\n"
        for mot, occurrence in occurrences_mots_recherches.items():
            occurences_affichage += f"{mot} : {occurrence}\n"

        # Vérification de la présence de balises alt
        balises_alt_presentes = re.findall(r'<img\s[^>]*alt="([^"]*)"[^>]*>', texte_page, re.IGNORECASE)
        if balises_alt_presentes:
            balises_alt = "\nBalises ALT présentes.\n"
        else:
            balises_alt = "\nBalises ALT non présentes.\n"

        # Filtrer les mots parasites
        structure_donnees_filtrees = Filtrage.filtrer_mots_parasites(structure_donnees, mots_parasites)
        mots_cles_filtres = "\nMots clés filtrés :\n"
        for mot, occurrence in structure_donnees_filtrees[:3]:
            mots_cles_filtres += f"{mot} : {occurrence}\n"

        # Afficher le texte récupéré sur le site dans la fenêtre
        self.texte_recupere.delete(1.0, tk.END)  # Effacer le texte précédent s'il existe
        self.texte_recupere.insert(tk.END, texte_nettoye)

        # Affichage des résultats
        self.resultats_label.config(text=occurences_affichage + mots_cles + infos_liens + balises_alt + mots_cles_filtres)


if __name__ == '__main__':
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()
