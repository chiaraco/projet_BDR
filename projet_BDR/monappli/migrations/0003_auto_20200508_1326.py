# Generated by Django 2.2.5 on 2020-05-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monappli', '0002_auto_20200508_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='degats',
            field=models.CharField(default=float("nan"), max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='emplacement',
            field=models.CharField(default=float("nan"), max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='nature',
            field=models.CharField(default=float("nan"), max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='phase_de_vol',
            field=models.CharField(default=float("nan"), max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accident',
            name='statut',
            field=models.CharField(default=float("nan"), max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='aeroport',
            name='iata',
            field=models.CharField(default=float("nan"), max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='aeroport',
            name='oaci',
            field=models.CharField(default=float("nan"), max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='avion',
            name='iata',
            field=models.CharField(default=float("nan"), max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='avion',
            name='oaci',
            field=models.CharField(default=float("nan"), max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='compagnie',
            name='alias',
            field=models.CharField(default=float("nan"), max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='compagnie',
            name='iata',
            field=models.CharField(default=float("nan"), max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='compagnie',
            name='oaci',
            field=models.CharField(default=float("nan"), max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='pays',
            name='iso',
            field=models.CharField(default=float("nan"), max_length=3, null=True),
        ),
    ]
