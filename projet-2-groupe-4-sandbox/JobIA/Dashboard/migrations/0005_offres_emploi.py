# Generated by Django 4.0.2 on 2022-02-25 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0004_delete_offres_emploi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offres_emploi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_offre', models.CharField(max_length=100)),
                ('intitule', models.CharField(max_length=100)),
                ('lieu', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('nom_entreprise', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('lien', models.CharField(max_length=100)),
                ('mots_clefs', models.CharField(max_length=200)),
            ],
        ),
    ]