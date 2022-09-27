from request_api_pe import request_api_pe
from job_extraction import job_pe_extraction, id_text
from request_api_azure import get_documents_key_phrases, scheduler, calcul_cout
from database import create_database, job_pe_to_db

db_name = "jobia.db"

print("Bonjour, entrez mots clés")
# key_word = input()
job_from_pe = request_api_pe('data')

jobs_extracted = job_pe_extraction(job_from_pe)
create_database(db_name)
job_pe_to_db(db_name, jobs_extracted)

# ---- Preparation appel API Azure ---------------

text_input_document = id_text(jobs_extracted)
calcul_cout(text_input_document, 0.80, 2)
#key_phrases = get_documents_key_phrases(text_input_document)