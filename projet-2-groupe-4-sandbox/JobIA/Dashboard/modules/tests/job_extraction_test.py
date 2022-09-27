import re
import datetime
from typing import List, Dict, Any
import pandas as pd


def job_pe_extraction(data_json: Dict[str, list]) -> Dict[str, List[Any]]:

    data = {
        "intitule": [],
        "lieu": [],
        "date": [],
        "nom_entreprise": [],
        "description": [],
        "lien": []}

    for i in range(len(data_json['resultats'])):

        try:
            regex = r'(?P<departement>\d{2})\s*[\W]*(?P<ville>[^\d]*)|.*'
            lieu = data_json['resultats'][i]['lieuTravail']['libelle']
            matching = re.search(regex, lieu)

            if matching.group("ville"):
                lieu = matching.group("ville")
                data["lieu"].append(lieu.lower())

            elif matching.group("departement"):
                lieu = matching.group("departement")
                data["lieu"].append(lieu.lower())
            else:
                lieu = data_json['resultats'][i]['lieuTravail']['libelle']
                data["lieu"].append(lieu.lower())

            date = data_json['resultats'][i]['dateCreation']
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')

            data["intitule"].append(data_json['resultats'][i]['intitule'])
            data["date"].append(date.date())
            data["lien"].append(data_json['resultats'][i]['origineOffre']["urlOrigine"])
            data["description"].append(data_json['resultats'][i]['description'])

            if "nom" in data_json['resultats'][i]['entreprise']:
                data["nom_entreprise"].append(data_json['resultats'][i]['entreprise']["nom"])
            else:
                data["nom_entreprise"].append("Unknow")
        except:

            if matching.group("ville"):
                print(f'lieu : {lieu} / matching : {matching.group("ville")} type {type(matching.group("ville"))}')
            else:
                print(
                    f'lieu : {lieu} / matching : {matching.group("departement")} type {type(matching.group("departement"))}')

    print("Pole emploi Job extraction: DONE")
    df_data = pd.DataFrame(data)
    df_data.to_csv("jobs.csv",sep=',', header=True)
    return data


def id_text(data: Dict[str, list]) -> List[Dict]:

    text_input_docs = []

    for id, description in enumerate(data["description"]):
        text_input_docs.append({"id": id, "text": description})

    return text_input_docs
