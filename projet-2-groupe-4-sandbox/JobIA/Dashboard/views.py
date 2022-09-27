from urllib import request
from django.shortcuts import render, redirect
from .forms import NewUserForm, Skills_for_user
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.template import loader
from django.http import HttpResponse
import os
import csv
from datetime import date

# from .modules.database import get_all_offres_emploi_brut
from .modules.database import get_all_skills, insert_offres_emploi_to_db, insert_skills_to_db, insert_offres_emploi_skills_to_db, insert_user_skills_to_db, get_offres_with_skills_and_user, get_count_skills
from .modules.job_extraction import job_pe_extraction
from  Dashboard.modules.database import insert_offres_emploi_to_db
from .models import Offres_emploi_brut
from .modules.request_api_pe import request_api_pe, pikle_keys
import pickle
from .modules.tests.main_test import pipeline_data


def user_select_skills(request):
    if request.method == "POST":
        form = Skills_for_user(request.POST)
        if form.is_valid():
            user_skills = form.cleaned_data
            print(user_skills)
            user = request.user
            if user != None:
                insert_user_skills_to_db(user.id, user_skills["skills"])

            messages.success(request, "Enregistrement effectué" )
            return redirect("login")
        messages.error(request, "Invalid enregistrement, informations erronées")
    form = Skills_for_user()
    
    return render (request=request, template_name="registration/skills.html", context={"register_form":form})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Enregistrement effectué" )
			return redirect("skills")
		messages.error(request, "Invalid enregistrement, informations erronées")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Vous êtes maintenant connecté en tant que {username}.")
				return redirect("home")
			else:
				messages.error(request,"Mot de passe invalid")
		else:
			messages.error(request,"Nom d'utilisateur ou mot de passe invalid")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Vous êtes bien déconnecté") 
	return redirect("home")


def insert_offres_emploi_brut():
    print("INSERT Dashboard_offres_emploi_brut")
    path = os.path.abspath("../JobIA/Offres_pe.csv")
    data_reader = []

    with open(path) as f:
        data_reader= csv.reader(f,  delimiter='|', quotechar='"')
        header = next(data_reader)
        
        i = 0
        for row in data_reader:
            offre_pe = Offres_emploi_brut()
            offre_pe.id_offre = row[0]
            offre_pe.intitule = row[1]
            offre_pe.description = row[2]
            offre_pe.dateCreation = row[3]
            offre_pe.dateActualisation = row[4]
            offre_pe.lieuTravail = row[5]
            offre_pe.romeCode = row[6]
            offre_pe.romeLibelle = row[7]
            offre_pe.appellationlibelle = row[8]
            offre_pe.entreprise = row[9]
            offre_pe.typeContrat = row[10]
            offre_pe.typeContratLibelle = row[11]
            offre_pe.natureContrat = row[12]
            offre_pe.experienceExige = row[13]
            offre_pe.experienceLibelle = row[14]
            offre_pe.salaire = row[15]
            offre_pe.alternance = row[16]
            offre_pe.nombrePostes = row[17]
            offre_pe.accessibleTH = row[18]
            offre_pe.qualificationCode = row[19]
            offre_pe.qualificationLibelle = row[20]
            offre_pe.secteurActivit = row[21]
            offre_pe.secteurActiviteLibelle = row[22]
            offre_pe.origineOffre = row[23]
            offre_pe.dureeTravailLibelleConverti = row[24]
            offre_pe.deplacementLibelle = row[25]
            offre_pe.offresManqueCandidats = row[26]
            offre_pe.dureeTravailLibelle = row[27]
            offre_pe.contact = row[28]
            offre_pe.qualitesProfessionnelles = row[29]
            offre_pe.competences = row[30]
            offre_pe.deplacementCode = row[31]
            offre_pe.permis = row[32]
            offre_pe.langues = row[33]
            offre_pe.formations = row[34]
            offre_pe.experienceCommentaire = row[35]
            offre_pe.agence = row[36]
            offre_pe.complementExercice = row[37]

            offre_pe.save()
            i +=1
    print(i)
    print("END INSERT Dashboard_offres_emploi_brut")

# def insert_offres_emploi(offres_emploi:list):
def insert_offres_emploi():

    print("INSERT Dashboard_offres_emploi")
    # pipeline_data()
    path = os.path.abspath("../JobIA/jobs.csv")
    data_reader = []

    jobs_extracted = []
    with open(path) as f:
        data_reader= csv.reader(f,  delimiter=',', quotechar='"')
        header = next(data_reader)
        for row in data_reader:
            jobs_extracted.append(row)


    insert_offres_emploi_to_db(jobs_extracted)

    print("END INSERT Dashboard_offres_emploi")

def insert_skills():

    print("INSERT Dashboard_skills")

    user_skills = ["sql", "python", "base de données", "data",
                "database", "data visualisation", "business intelligence", "power bi", "tableau", "prediction",
                "intelligence artificielle", "classification", "regression", "api", "pandas", "scikitlearn", "numpy",
                "flask",
                "django", "gestion", "projet", "agile", "scrum", "workflow", "etl", "pipeline", "machine learning", "télétravail"]
    insert_skills_to_db(user_skills)

    print("END INSERT Dashboard_skills")

def insert_asso_offres_emploi_skills():
    insert_offres_emploi_skills_to_db()

def index(request):
    return HttpResponse("")

def home_page(request):
    template = loader.get_template("dashboard/homepage.html")
    user_id = ""
    context = {
        "date" : date.today(),
    }
    if request.user != None:
        user_id = request.user.id
    
        list_offres_a_afficher = []
        if user_id != None:
            # count_skills = get_count_skills(user_id)
            # count_skill = count_skills[0][0]
            precision = 0
            count_skill = 5        
            print(count_skill)
            if int(count_skill) > 0:
                list_offres, list_precision_offres = get_offres_with_skills_and_user(user_id)

                for id in range(len(list_offres)):
                    precision = list_precision_offres[id]
                    if int(list_precision_offres[id]) > count_skill:
                        precision = count_skill
                    list_offres_a_afficher.append([list_offres[id], (int(precision)/5*100)])

                list_moins_que_trente = []
                list_plus_que_trente = []
                list_plus_que_soixante = []

                for pourcentage in list_offres_a_afficher:
                    if pourcentage[1] < 30:
                        list_moins_que_trente.append(pourcentage[1])
                    elif pourcentage[1] >= 30 and pourcentage[1] < 60:
                        list_plus_que_trente.append(pourcentage[1])
                    else:
                        list_plus_que_soixante.append(pourcentage[1])

                context = {
                    "date" : date.today(),
                    "list_offres": list_offres_a_afficher,
                    "moins_que_trente": len(list_moins_que_trente),
                    "plus_que_trente" : len(list_plus_que_trente),
                    "plus_que_soixante" : len(list_plus_que_soixante)
                }
    return HttpResponse(template.render(context, request))
