# importation du module csv en python
import csv

# déclaration de tableau vide pour recevoir les données
data = []

# Ouverture de notre fichier en mode lecture

f = open(r"/home/biglaye/Documents/Sonatel_academy/PYTHON/PROJET/Données Projet.xlsx - Feuil2.csv")
myReader = csv.reader(f)

for row in myReader:
    if row[2] != "" and row[3] != "":
        data.append(row)
# data = [row for row in myReader] # creation de notre tableau de donnéés en utilisant les lignes


invalide = [data[0]]
valide = [data[0]]

for elem in data:  # suppression du premier element de chaque ligne
    del elem[0:1]


# verification de la validité du numéro d'étudiant
def bon_numero(chaine):
    res = False
    number = [str(i) for i in range(10)]
    if len(chaine) == 7 and chaine.isupper() and chaine.isalnum():
        for elem in chaine:
            if elem in number:
                res = True
                break
    else:
        res = False
    return res


# verification de la validité du nom d'étudiant
def valide_nom(prenom, nom):
    count_nom = 0
    count_prenom = 0
    if (prenom[0].isalpha and nom[0].isalpha):
        for n in nom:
            if n.isalpha:
                count_nom += 1
        for p in prenom:
            if p.isalpha:
                count_prenom += 1
        if count_nom >= 2 and count_prenom >= 3:
            return True
    else:
        return False


# formatage de la date
def date(chaine):
    sep = "/-.,:;_- '"
    mois = {"ja": "1", "f": "2", "mars": "3", "av": "4", "mai": "5", "juin": "6",
            "juil": "7", "ao": "8", "sep": "9", "oct": "10", "nov": "11", "dec": "12"}
    chaine = chaine.strip()
    for elem in chaine:
        if elem in sep:
            chaine = chaine.replace(elem, "/")
    chaine = chaine.split("/")
    chaine = [chaine[i] for i in range(len(chaine)) if len(chaine[i]) != 0]
    for keys in mois:
        if str(chaine[1].lower()).startswith(keys):
            chaine[1] = mois[keys]
            break
    return "/".join(chaine)


# verification de la validité de la classe
def classe_valide(chaine):
    chaine = chaine.strip()
    if len(chaine) == 0:
        return False
    else:
        if chaine[0] in [str(i) for i in range(3, 7)] and chaine[-1] in ["A", "B"]:
            return True
        else:
            return False


def note(A):
    char_liste = ":;"
    sep = "# "
    B = A
    A = A.replace(",", ".")
    for elem in A:
        if elem in char_liste:
            A = A.replace(elem, ",")
    for elem in A:
        if elem in sep:
            A = A.replace(elem, "")
    A = (" ").join(A.split("["))
    A = (" ").join(A.split("]"))
    A = A.split()
    if len(A) % 2 == 0:
        dct = {A[i]: [(A[i + 1])] for i in range(0, len(A), 2)}
        dic = {}
        for mat in dct:
            s = dct[mat]
            dic[mat] = [elem for elem in ("").join(s).split(",") if elem != '']
        return dic
    else:
        return B


## Validité d'une date
def validite_date(c):
    c = c.strip()
    if len(c) == 0:
        return False
    else:
        c = c.split("/")
        if int(c[0]) < 1 or int(c[0]) > 31 or int(c[1]) < 1 or int(c[1]) > 12 or ((c[1] == 2) and (int(c[0]) > 29) and (
                (int(c[2]) % 4 == 0 and int(c[2]) % 100 != 0) or int(c[2]) % 400 == 0)) or (
                (int(c[1]) == 2) and (int(c[0]) > 28) and (
                (int(c[2]) % 4 != 0 or int(c[2]) % 100 == 0) and int(c[2]) % 400 != 0)):
            return False
        else:
            return True


# Fonction pour verifier si un chaine contient une lettre
def verif_lettre(chaine):
    p = 0
    for elem in range(len(chaine)):
        if chaine[elem].isalpha():
            p += 1
    if p >= 1:
        return True
    else:
        return False


# Fonction qui verifie sur un nombre contient deux points

def verf(num):
    p = 0
    for elem in num:
        if elem == ".":
            p += 1
    if p >= 2:
        return True
    else:
        return False


for i in range(1, len(data)):
    if data[i][5] != "":
        data[i][5] = note(data[i][5])

for i in range(1, len(data)):
    if data[i][3] != "":
        data[i][3] = date(data[i][3])

for i in range(1, len(data)):
    if bon_numero(data[i][0]) and validite_date(data[i][3]) and classe_valide(data[i][4]):
        if type(data[i][5]) == str:
            invalide.append(data[i])
        else:
            vide = []
            p = 0
            #             for elem in data[i][5].values():
            #                 vide.extend(elem)
            for elem in data[i][5].values():
                vide.extend(elem)
            for s in vide:
                if verf(s) or float(s) > 20:
                    p = p + 1
            if p >= 1:
                invalide.append(data[i])
            else:
                valide.append(data[i])
    else:
        invalide.append(data[i])

# Données valide dans un fichier nommé fichier

fichier = valide.copy()
fichier

# Dictionnaire de données valides
# Clés du dictionnaire

key = [k for k in fichier[0]]
key

# Valeurs dictionnaire

value = []

for i in range(6):
    d = []
    j = 1
    while j < len(fichier):
        d.append(fichier[j][i])
        j += 1
    value.append(d)

dico = dict(zip(key, value))

# changement du type des notes en float

for i in range(len(dico["Numero"])):
    for c, v in dico["Note"][i].items():
        dico["Note"][i][c] = [float(elem) for elem in v]

# Moyennes des notes pour chaque matière

dico["Moyennes"] = [{c: round((sum(v[:-1]) / len(v[:-1]) + 2 * v[-1]) / 3) for c, v in dico["Note"][i].items()} for i in
                    range(len(dico["Numero"]))]

# Total des notes pour chaque eleve

dico["Moyenne general"] = [sum(dico["Moyennes"][i].values()) / 5 for i in range(len(dico["Numero"]))]

# Affichage de tous les eleves

for i in range(len(dico["Numero"])):
    for c, v in dico.items():
        print(c, v[i])
        print("\t")

# ## Affichage des données valide et/ou invalide


while True:
    print("""
    1.Voir les données valides
    2.Voir les données invalides
    0.Exit/Quit
    """)
    choix = int(input("Que voulez-vous faire ? "))
    if choix == 2:
        for elem in invalide:
            print(elem, end="\n\n")
    elif choix == 1:
        for i in range(len(dico["Numero"])):
            for c, v in dico.items():
                print (c, v[i])
                print("\n")
    elif choix == 0:
        print("Au revoir !")
        break
    else:
        print("Choix indisponible")

# ## Afficher d'une information par son numéro

while True:
    print("""
    1.Voir les informations d'un étudiant
    0.Exit/Quit
    """)
    choix = int(input("Que voulez-vous faire ? "))
    if choix == 1:
        inv = [invalide[i][0] for i in range(len(invalide))]
        num = input("Donner le numéro dont vous voulez voir les informations ")
        if num in dico["Numero"]:
            i = dico["Numero"].index(num)
            for c, v in dico.items():
                        print (c, v[i])
        elif num in inv:
            i = inv.index(num)
            print(invalide[i])
            print("Ces données sont manquantes et/ou incorret ")
        else:
            print("Le numéro saisi n'est pas dans la base de données")
    elif choix == 0:
        print("Au revoir !")
        break
   

# # Affichage des cinq premiers


indice = [i for i in range(len(dico["Moyenne general"]))]  # recuperuration de indice des totaux dans dico
tup_indice = [(dico["Moyenne general"][i], i) for i in indice]  # tuple des indices de chaque total
s = sorted(tup_indice)
print("Voici les 5 premier du classement général \n")
for i in range(1, 6):
    pos = s[-i][1]
    print(dico["Prénom"][pos], dico["Nom"][pos], dico["Classe"][pos], s[-i][0], "de moyenne")
    print("\n")
