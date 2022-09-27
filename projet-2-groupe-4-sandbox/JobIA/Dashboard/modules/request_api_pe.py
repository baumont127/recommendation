import imp
import json
import os
from black import main

from dotenv import load_dotenv
from offres_emploi import Api
import csv
import pickle


load_dotenv()


def request_api_pe(*args):

    """
    La fonction requete l'API pole emploi afin d'obtenir les offres d'emploi disponible avec
    le mots clé data Output : Json
    """
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    client = Api(client_id=client_id, client_secret=client_secret)

    for word in args:

        params = {
            "motsCles": word,
            "region": 84,
            "sort": 1
        }

        basic_search = client.search(params=params)

    print("Pole Emploi API request : DONE")
    return basic_search

def pikle_keys():
    list_of_list_terms = pickle.load(open("../JobIA/terms.pickle", "rb"))
    return list_of_list_terms

def create_csv_offres_brut(pe_request: json):
    with open('Offres_pe.csv', 'w', encoding='UTF8') as f:
        csv_columns = ['id', 'intitule', 'description', 'dateCreation', 'dateActualisation', 'lieuTravail', 'romeCode', 'romeLibelle', 'appellationlibelle', 'entreprise', 'typeContrat', 'typeContratLibelle', 'natureContrat', 'experienceExige', 'experienceLibelle', 'salaire', 'alternance', 'nombrePostes', 'accessibleTH', 'qualificationCode', 'qualificationLibelle', 'secteurActivite', 'secteurActiviteLibelle', 'origineOffre', 'dureeTravailLibelleConverti', 'deplacementLibelle', 'offresManqueCandidats', 'dureeTravailLibelle', 'contact', 'qualitesProfessionnelles', 'competences', 'deplacementCode', 'permis', 'langues', 'formations','experienceCommentaire','agence', 'complementExercice']
        writer = csv.DictWriter(f, fieldnames=csv_columns, delimiter ="|")
        writer.writeheader()
        for dict_request in pe_request["resultats"]:
            writer.writerow(dict_request)

if __name__ == "__main__" :
    pe_request = request_api_pe("data")
    create_csv_offres_brut(pe_request)



