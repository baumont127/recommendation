import sqlite3
from typing import List, Dict
from ..modules.request_api_pe import pikle_keys
from ..models import Offres_emploi, Skills, Asso_offres_emploi_skills, Asso_user_skills
from django.contrib.auth.models import User
from ..modules.job_matching import job_match, matching_score


def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Create table job_pe
    cur.execute('''DROP TABLE IF EXISTS job_pe ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS job_pe
               (intitule,
        nom_entreprise,
        lieu, date,
        lien, description)''')

    # Create table simplon_skills
    cur.execute('''DROP TABLE IF EXISTS simplon_skills ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS simplon_skills
               (skills)''')

    conn.commit()
    cur.close()
    conn.close()
    print("Database Creation DONE")
    return


def job_pe_to_db(db_name: str, data: Dict[str, List]):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for i in range(len(data["intitule"])):
        db_line = (data["intitule"][i],
                   data["lieu"][i],
                   data["date"][i],
                   data["nom_entreprise"][i],
                   data["description"][i],
                   data["lien"][i])

        requete = f'''INSERT INTO job_pe VALUES(?,?,?,?,?,?)'''
        # print(requete, db_line)
        cur.execute(requete, db_line)

        conn.commit()
    cur.close()
    conn.close()
    print("job_pe insertion: DONE ")
    return


def simplon_skills_to_db(db_name: str):
    simplon_skills = ["sql", "python", "base de données", "data",
                      "database", "data visualisation", "business intelligence", "power bi", "tableau", "prediction",
                      "intelligence artificielle", "classification", "regression", "api", "pandas", "scikitlearn", "numpy", "flask",
                      "django", "gestion", "projet", "agile", "scrum", "workflow", "etl", "pipeline","machine learning"]

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for i in range(len(simplon_skills)):
        db_line = (simplon_skills[i])
        requete = f'''INSERT INTO simplon_skills VALUES(?)'''
        cur.execute(requete, (db_line,))
        conn.commit()
    cur.close()
    conn.close()
    print("Simplon skills insertion: DONE ")
    return

def get_all_offres_emploi_brut():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = '''SELECT * FROM Dashboard_offres_emploi_brut;'''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()

    return response

def get_all_offres_emploi():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = '''SELECT * FROM Dashboard_offres_emploi;'''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()

    return response

def get_all_skills():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = '''SELECT * FROM Dashboard_skills;'''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()

    return response

def get_count_skills(user_id):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = f'''SELECT count(*) FROM Dashboard_asso_user_skills WHERE Dashboard_asso_user_skills.user_id = {user_id}'''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()
    return response

def get_offres_with_skills():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = '''
                SELECT *
                FROM
                    Dashboard_offres_emploi, Dashboard_asso_offres_emploi_skills
                WHERE 
                    Dashboard_asso_offres_emploi_skills.offres_emploi_id = Dashboard_offres_emploi.id 
                AND
                    Dashboard_asso_offres_emploi_skills.skills_id = (SELECT id FROM Dashboard_skills WHERE Dashboard_skills.mot_clef = "sql");
    '''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()

    return response


def select_skills_id_with_user(user_id):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = f'''SELECT skills_id FROM Dashboard_asso_user_skills WHERE Dashboard_asso_user_skills.user_id = {user_id};
    '''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()

    return response

def select_offres_emploi_id_with_skills_id(skills_id):
    list_skills_id_req = []
    for id in skills_id:
        list_skills_id_req.append(id[0])

    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = f'''
    SELECT precision, offres_emploi_id FROM Dashboard_asso_offres_emploi_skills 
	WHERE Dashboard_asso_offres_emploi_skills.id in {tuple(list_skills_id_req)};
    '''
    cur.execute(requete)
    response = cur.fetchall()
    cur.close()
    conn.close()

    return response

def select_offres_emploi_with_id(offres_emploi_id_with_precision):
    list_offres_emploi_id_req = []
    list_precision_offres = []
    for offre_precision in offres_emploi_id_with_precision:
        list_precision_offres.append(offre_precision[0])    
        list_offres_emploi_id_req.append(offre_precision[1])

    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    requete = f'''
    SELECT * from Dashboard_offres_emploi 
	WHERE Dashboard_offres_emploi.id in {tuple(list_offres_emploi_id_req)};
    '''
    cur.execute(requete)
    list_offres_emploi = cur.fetchall()
    cur.close()
    conn.close()
    return list_offres_emploi, list_precision_offres


def get_offres_with_skills_and_user(user_id):

    if user_id != None:
        skills_id = select_skills_id_with_user(user_id)
        offre_emploi_id_with_precision = select_offres_emploi_id_with_skills_id(skills_id)
        list_offres_emploi, list_precision = select_offres_emploi_with_id(offre_emploi_id_with_precision)

        return list_offres_emploi, list_precision

    return ()

def insert_offres_emploi_to_db(data: list):
    list_of_list_terms = pikle_keys()

    for i, list_offres in enumerate(data):
        Key_phrases = []
        for list_of_terms in list_of_list_terms:
            for term in list_of_terms:
                if i == int(term.id):
                    Key_phrases = term.key_phrases
        
        offre_pe = Offres_emploi()
        offre_pe.intitule = list_offres[1]
        offre_pe.lieu = list_offres[2]
        offre_pe.date = list_offres[3]
        offre_pe.nom_entreprise = list_offres[4]
        offre_pe.description = list_offres[5]
        offre_pe.lien = list_offres[6]
        offre_pe.mots_clefs = Key_phrases
        offre_pe.save()

def insert_skills_to_db(list_skills : list):
    
    for skill in list_skills:
        skill_db = Skills()
        skill_db.mot_clef = skill
        skill_db.save()

def insert_offres_emploi_skills_to_db():

    simplon_skills = get_all_skills()
    list_skills = []

    for skill in simplon_skills:
        list_skills.append(skill[1])

    key_terms = pikle_keys()
    match =  job_match(key_terms, list_skills)
    matching = matching_score(match)

    for i in range(len(match)):
        for skill in simplon_skills:
            for match_skill in match[i]["matching_terms"]:
                if match_skill == skill[1]:
                    for j in range(len(matching)):
                        if matching[j]["id"] == match[i]["id"]:
                            skill_id = Skills.objects.get(pk= int(skill[0]))
                            offre_emploi_id = Offres_emploi.objects.get(pk= int(match[i]["id"]))
                            Asso_offres_emploi_skills_db = Asso_offres_emploi_skills()
                            Asso_offres_emploi_skills_db.precision = matching[j]["matching_score"]
                            Asso_offres_emploi_skills_db.skills = skill_id
                            Asso_offres_emploi_skills_db.offres_emploi = offre_emploi_id
                            Asso_offres_emploi_skills_db.save()

def insert_user_skills_to_db(user_id, list_skills):
    for skill in list_skills:
        print("user_id : ", user_id, "skill_id : ", skill)
        asso_user_skills_db = Asso_user_skills()
        asso_user_skills_db.skills = Skills.objects.get(pk= int(skill))
        asso_user_skills_db.user = User.objects.get(pk = user_id)
        asso_user_skills_db.save()
