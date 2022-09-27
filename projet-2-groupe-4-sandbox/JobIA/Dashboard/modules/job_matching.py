from typing import List, Dict


def job_match(job_key_terms: list, user_skills: list):
    
    # user_skills = ["sql", "python", "base de données", "data",
    #                "database", "data visualisation", "business intelligence", "power bi", "tableau", "prediction",
    #                "intelligence artificielle", "classification", "regression", "api", "pandas", "scikitlearn", "numpy",
    #                "flask",
    #                "django", "gestion", "projet", "agile", "scrum", "workflow", "etl", "pipeline", "machine learning", "télétravail"]

    job_matching = []
    term_matching = []

    for i in range(len(job_key_terms)):
        for j in range(len(job_key_terms[i])):
            for key_term in job_key_terms[i][j].key_phrases:
                if key_term.lower() in user_skills and key_term.lower() not in term_matching:
                    term_matching.append(key_term.lower())
            if len(term_matching) > 0:
                job_matching.append({"id": job_key_terms[i][j].id, "matching_terms": term_matching})
                term_matching = []

    return job_matching


def sort_by_match(job):
    return job["matching_score"]


def matching_score(job_matching: List[Dict]):
    matching = []

    for job in job_matching:
        matching.append({"id": job["id"], "matching_score": len(job["matching_terms"])})

    matching.sort(key=sort_by_match, reverse=True)
    return matching
