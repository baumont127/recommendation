import csv
import os
import pickle
from typing import List, Dict
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
cog_key = os.getenv("COG_SERVICE_KEY")


def detect_language_sdk(documents: list) -> List[object]:
    credential = AzureKeyCredential(cog_key)
    client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)
    results = client.detect_language(documents=documents)

    # detected_language = results[0].primary_language
    # language = detected_language.name
    # language_code = detected_language.iso6391_name
    # confidence = detected_language.confidence_score

    return results


def extract_main_terms_sdk(documents: list) -> List[object]:
    # create the Azure Key Credential object with the secret key (use `cog_key`)
    credential = AzureKeyCredential(cog_key)

    # create the Azure Text Analytics Client object with the endpoint (use `cog_endpoint`) and the credential object
    client = TextAnalyticsClient(cog_endpoint, credential)

    # call the `extract_key_phrases` method with the list of documents
    results = client.extract_key_phrases(documents)

    return results


def get_documents_key_phrases(documents: List[Dict]) -> List[object]:
    terms = []
    languages = detect_language_sdk(documents)
    list_docs = []
    for id_docs in range(0, len(documents)):
        for id_languages in range(0, len(languages)):
            if int(documents[id_docs]["id"]) == (id_languages + 1):
                docs = {}
                docs["id"] = documents[id_docs]["id"]
                docs["text"] = documents[id_docs]["text"]
                docs["language"] = languages[id_languages].primary_language.iso6391_name
                list_docs.append(docs)

    batch_of_docs = scheduler(list_docs)
    for batch in batch_of_docs:
        terms.append(extract_main_terms_sdk(batch))

    print(terms)
    pickle.dump(terms, open("terms.pickle", "wb"))

    return terms


def scheduler(documents: List[Dict]) -> List[List[Dict]]:
    list_elements = []
    list_documents = []
    index_cut = 0
    for document in documents:
        if index_cut < 10:
            list_documents.append(document)
            index_cut += 1

        if index_cut == 10:
            list_elements.append(list_documents)
            list_documents = []
            index_cut = 0

    if (index_cut > 0):
        list_elements.append(list_documents)

    return list_elements


def calcul_cout(documents: list, prix_unite: float, nb_apis: int):

    unites = 0
    for elem in documents:
        count_characters = len(elem["text"])
        if (count_characters / 1000) > (int(count_characters / 1000)):
            if count_characters / 1000 < 1:
                unites += 1
            else:
                unites += (int(count_characters / 1000) + 1)
        else:
            unites += (count_characters / 1000)

    prix = (unites / 1000) * prix_unite
    print(f"Calcul du coût (API Azure) : {prix*nb_apis}")
    return unites, (prix * nb_apis)


if __name__ == "__main__":
    with open("Annonce.txt", 'r') as f:
        text = f.read(5120)

    with open("Annonce_2.txt", 'r') as f:
        text_2 = f.read(5120)

    with open("Annonce_3.txt", 'r') as f:
        text_5 = f.read(5120)

        text_3 = text
        text_4 = text
