from Dashboard.modules.request_api_pe import request_api_pe
from Dashboard.modules.tests.job_extraction_test import job_pe_extraction, id_text
from Dashboard.modules.tests.request_api_azure_test import get_documents_key_phrases, scheduler, calcul_cout
from Dashboard.modules.database import create_database
# from Dashboard.modules.database import create_database, job_pe_raw_to_db
from Dashboard.modules.request_api_pe import create_csv_offres_brut
import pickle

def pipeline_data():
    job_from_pe = request_api_pe('data')
    create_csv_offres_brut(job_from_pe)

    jobs_extracted = job_pe_extraction(job_from_pe)
    text_input_document = id_text(jobs_extracted)
    calcul_cout(text_input_document, 0.80, 2)
    # get_documents_key_phrases(text_input_document)


if  __name__ == "__main__" :
    # db_name = "jobia.db"

    # print("Bonjour, entrez mots clés")
    #key_word = input()
    job_from_pe = request_api_pe('data')
    create_csv_offres_brut(job_from_pe)

    jobs_extracted = job_pe_extraction(job_from_pe)
    # create_database(db_name)
    # job_pe_raw_to_db(db_name, jobs_extracted)

    # ---- Preparation appel API Azure ---------------

    text_input_document = id_text(jobs_extracted)
    calcul_cout(text_input_document, 0.80, 2)
    # key_phrases = get_documents_key_phrases(text_input_document)

    # terms = pickle.load(open("../terms.pickle", "rb"))
    # print(type(terms[0][0].id))
    # print(terms[0][0])
    # print(terms.key_phrases)


    ### ANCIEN REPO

    # from modules.request_api_pe import request_api_pe
    # from job_extraction_test import job_pe_extraction, id_text
    # from request_api_azure_test import get_documents_key_phrases, scheduler, calcul_cout
    # from modules.database import create_database, job_pe_to_db, simplon_skills_to_db
    # from modules.job_matching import job_match, matching_score
    # import pickle

    # db_name = "jobia.db"

    # job_from_pe = request_api_pe('data')

    # jobs_extracted = job_pe_extraction(job_from_pe)
    # create_database(db_name)
    # job_pe_to_db(db_name, jobs_extracted)

    # # ---- Preparation appel API Azure ---------------

    # text_input_document = id_text(jobs_extracted)
    # simplon_skills_to_db(db_name)
    # calcul_cout(text_input_document, 0.80, 2)
    # job_key_terms = pickle.load(open("../terms.pickle", "rb"))
    # matching = job_match(job_key_terms)
    # match_score = matching_score(matching)

    # for score in match_score:
    #     print(score)