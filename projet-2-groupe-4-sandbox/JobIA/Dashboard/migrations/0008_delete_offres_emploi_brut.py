# Generated by Django 4.0.2 on 2022-02-27 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0007_remove_offres_emploi_id_offre'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Offres_emploi_brut',
        ),
    ]
