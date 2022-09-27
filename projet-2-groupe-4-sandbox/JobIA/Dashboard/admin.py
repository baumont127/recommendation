from django.contrib import admin

# Register your models here.
from .models import Offres_emploi_brut, Offres_emploi, Skills, Metiers

admin.site.register(Offres_emploi_brut)
admin.site.register(Offres_emploi)
admin.site.register(Skills)
admin.site.register(Metiers)