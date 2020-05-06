# Generated by Django 2.2.5 on 2020-05-06 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monappli', '0004_ville'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aeroport',
            fields=[
                ('IdAeroport', models.AutoField(primary_key=True, serialize=False)),
                ('NomAeroport', models.CharField(max_length=200)),
                ('IATA', models.CharField(max_length=3)),
                ('OACI', models.CharField(max_length=4)),
                ('Ville', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monappli.Ville')),
            ],
        ),
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('IdAccident', models.AutoField(primary_key=True, serialize=False)),
                ('Emplacement', models.CharField(max_length=200)),
                ('Phase_de_vol', models.CharField(max_length=200)),
                ('Nature', models.CharField(max_length=200)),
                ('Statut', models.CharField(max_length=200)),
                ('Degats', models.CharField(max_length=200)),
                ('IdAeroport_arrivee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arrivee', to='monappli.Aeroport')),
                ('IdAeroport_depart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depart', to='monappli.Aeroport')),
                ('IdAvion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monappli.Avion')),
                ('NomCompagnie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monappli.Compagnie')),
                ('NomPays', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monappli.Pays')),
            ],
        ),
    ]
