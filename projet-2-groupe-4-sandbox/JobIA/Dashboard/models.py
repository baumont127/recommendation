from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Offres_emploi_brut(models.Model):
    id_offre = models.CharField(max_length=100)
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    dateCreation = models.CharField(max_length=100)
    dateActualisation = models.CharField(max_length=100)
    lieuTravail = models.CharField(max_length=100)
    romeCode = models.CharField(max_length=100)
    romeLibelle = models.CharField(max_length=100)
    appellationlibelle = models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100)
    typeContrat = models.CharField(max_length=100)
    typeContratLibelle = models.CharField(max_length=100)
    natureContrat = models.CharField(max_length=100)
    experienceExige = models.CharField(max_length=100)
    experienceLibelle = models.CharField(max_length=100)
    salaire = models.CharField(max_length=100)
    alternance = models.CharField(max_length=100)
    nombrePostes = models.CharField(max_length=100)
    accessibleTH = models.CharField(max_length=100)
    qualificationCode = models.CharField(max_length=100)
    qualificationLibelle = models.CharField(max_length=100)
    secteurActivit = models.CharField(max_length=100)
    secteurActiviteLibelle = models.CharField(max_length=100)
    origineOffre = models.CharField(max_length=100)
    dureeTravailLibelleConverti = models.CharField(max_length=100)
    deplacementLibelle = models.CharField(max_length=100)
    offresManqueCandidats = models.CharField(max_length=100)
    dureeTravailLibelle = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    qualitesProfessionnelles = models.CharField(max_length=100)
    competences = models.CharField(max_length=100)
    deplacementCode = models.CharField(max_length=100)
    permis = models.CharField(max_length=100)
    langues = models.CharField(max_length=100)
    formations = models.CharField(max_length=100)
    experienceCommentaire = models.CharField(max_length=100)
    agence = models.CharField(max_length=100)
    complementExercice = models.CharField(max_length=100)

class Skills(models.Model):
    mot_clef = models.CharField(max_length=100)

class Metiers(models.Model):
    nom = models.CharField(max_length=100)

class Offres_emploi(models.Model):
    intitule = models.CharField(max_length=100)
    lieu = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    nom_entreprise = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    lien = models.CharField(max_length=100)
    mots_clefs = models.CharField(max_length=200)

class Asso_user_skills(models.Model):
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Asso_offres_emploi_skills(models.Model):
    precision = models.CharField(max_length=100)
    skills = models.ForeignKey(Skills, on_delete=models.CASCADE)
    offres_emploi = models.ForeignKey(Offres_emploi, on_delete=models.CASCADE)

# class Asso_offres_emploi_metiers(models.Model):
#     precision = models.CharField(max_length=100)
#     metiers = models.ForeignKey(Metiers, on_delete=models.CASCADE)
#     user = models.ForeignKey(Offres_emploi, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/fr/4.0/ref/models/fields/#django.db.models.ManyToManyField