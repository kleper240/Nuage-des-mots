import os
import PyPDF2 as pd2
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd


# Chemin du répertoire contenant les fichiers PDF à convertir en fichiers texte
chemin_pdf = r"C:\Users\Marius Mabulu\OneDrive - UPEC\BUT1\Semestre 2\SAE\Exploration algorithmique d'un problème\nuage2\fichierpdf"

# Chemin du répertoire contenant les fichiers texte de sortie
chemin_txt = r"C:\Users\Marius Mabulu\OneDrive - UPEC\BUT1\Semestre 2\SAE\Exploration algorithmique d'un problème\nuage2\fichiertxt"

# Convertir les fichiers PDF en fichiers texte
for root, dirs, files in os.walk(chemin_pdf):
    for file in files:
        if file.endswith('.pdf'):
            # Chemin du fichier PDF à convertir
            chemin_fichier_pdf = os.path.join(root, file)

            # Chemin du fichier texte de sortie
            chemin_fichier_txt = os.path.join(chemin_txt, file[:-4] + ".txt")

            # Ouvrir le fichier PDF en lecture binaire
            with open(chemin_fichier_pdf, "rb") as fichier_pdf:
                # Créer un objet PyPDF2 pour le fichier PDF
                pdf = pd2.PdfReader(fichier_pdf)
                # Extraire le texte du fichier PDF
                texte = ""
                for i in range(len(pdf.pages)):

                    texte += pdf.pages[i].extract_text()


            # Écrire le texte extrait dans un fichier texte
            with open(chemin_fichier_txt, "w", encoding="utf-8") as fichier_txt:
                fichier_txt.write(texte)


# Analyser les fichiers texte et créer des graphes de fréquence de mots
chemin = os.path.dirname(os.path.abspath(__file__))


fichier_txt = []
for root, dirs, files in os.walk(chemin):
    for file in files:
        if file.endswith('.txt'):
            fichier_txt.append(os.path.join(root, file))


liste_de_dict= []
for fichier in (fichier_txt):
    try:
        with open(fichier, mode='r', encoding="utf8") as f:
            contenu = f.read()
            contenu = contenu.replace(',', '').replace('.', '').replace('’', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ')
            chaine = contenu.lower()
            texte = chaine.split()
            liste = ["plus","tout","sur ",'après', "pour","dans","avec", "même","pas", "par","oui","non","aux","les", "une", "des", "cet", "cette", "ces", "elle" , "nous", "vous", "ils", "elles", "nous", "vous", "leur", "lui", "eux", "elles", "moi", "toi", "soi","mon", "ton", "son", "notre", "votre", "leur","mien", "tien", "sien", "nôtre", "vôtre", "leur","ses","tes","mes","nos","vos","oui","mais","est","donc","car","qui","que","quoi", "ont", "tous"]
            doublon = [mot for mot in texte if len(mot) > 2 and mot not in liste]

            print(100 * "-")
            print(len(doublon))
            print(100 * "-")
            somme = len(doublon)

            compteur = {mot: round((doublon.count(mot)/somme)*100,2) for mot in doublon}

            dictionnaire_trie = dict(sorted(compteur.items(), key=lambda x: x[1]))
            #print(dictionnaire_trie)
            liste_de_dict.append(dictionnaire_trie)

            
            
        


            wordcloud = WordCloud(width=1200, height=1200, background_color='black', min_font_size=5).generate_from_frequencies(dictionnaire_trie)
           
            plt.figure(figsize=(8, 8), facecolor=None)
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.show()

            cles = list(dictionnaire_trie.keys())
            derniers_cles = cles[-7:]
            dernieres_valeurs = [dictionnaire_trie[cle] for cle in derniers_cles]
           
            plt.barh(derniers_cles,dernieres_valeurs)
            plt.show()
           
    except IOError:
        print("Erreur de lecture du fichier :", fichier)
                
# fonction pour calculer la distance entre deux dictionnaires
def calculer_distance(dict1, dict2):
    somme = 0
    normalise = 0
    for mot, valeur1 in dict1.items():
        if mot in dict2:
            valeur2 = dict2[mot]
            somme += abs((valeur1 - valeur2))
            normalise += 1
        else:
            somme += abs(valeur1)
    for mot , valeur2 in dict2.items():
        somme1 = 0
        normalise1 = 0
        if mot not in dict1:
            somme1 += abs(valeur2)
            normalise1 += 1
    S_somme = somme +somme1
    N_normalise = normalise + normalise1
    return S_somme/N_normalise

# obtenir la longueur de la liste
var = len(liste_de_dict)

# dictionnaire pour stocker les distances
dico_distance = {}

# boucle pour comparer tous les dictionnaires deux par deux
for i, dict1 in enumerate(liste_de_dict):
    # le deuxième élément de la boucle commence à i+1 pour éviter les duplications
    for j, dict2 in enumerate(liste_de_dict[i+1:], i+1):
        # calculer la distance entre les deux dictionnaires
        distance = calculer_distance(dict1, dict2)
        # stocker la distance dans le dictionnaire
        dico_distance[f"{i+1} et {j+1}"] = distance
        # afficher la distance pour chaque paire de dictionnaires
        print(f"La somme de la distance des mots est du texte{i+1} et texte{j+1} est : {distance}")

# obtenir les clés et les valeurs du dictionnaire de distances
cles = list(dico_distance.keys())
valeurs = list(dico_distance.values())

# afficher le graphique des distances
plt.bar(cles, valeurs)
plt.show()
