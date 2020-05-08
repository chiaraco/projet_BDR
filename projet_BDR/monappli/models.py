from django.db import models
import numpy as np

# Create your models here.
class Pays(models.Model):
	nom_pays = models.CharField(max_length=200,primary_key=True)
	iso = models.CharField(max_length=3,null=True,default=np.nan)

class Avion(models.Model):
	id_avion =  models.AutoField(primary_key=True)
	modele = models.CharField(max_length=200,unique=True)
	iata = models.CharField(max_length=3,null=True,default=np.nan)
	oaci = models.CharField(max_length=4,null=True,default=np.nan)
	
class Compagnie(models.Model):
	nom_compagnie = models.CharField(max_length=200,primary_key=True)
	alias = models.CharField(max_length=30,null=True,default=np.nan)
	iata = models.CharField(max_length=3,null=True,default=np.nan)
	oaci = models.CharField(max_length=3,null=True,default=np.nan)
	nom_pays = models.ForeignKey(Pays, on_delete=models.SET_NULL,null=True)

class Ville(models.Model):
	id_ville =  models.AutoField(primary_key=True)
	nom_ville = models.CharField(max_length=200)
	nom_pays = models.ForeignKey(Pays, on_delete=models.SET_NULL,null=True)

class Aeroport(models.Model):
	id_aeroport = models.AutoField(primary_key=True)
	nom_aeroport = models.CharField(max_length=200,unique=True)
	iata = models.CharField(max_length=3,null=True,default=np.nan)
	oaci = models.CharField(max_length=4,null=True,default=np.nan)
	latitude = models.FloatField(null=True,default=None)
	longitude = models.FloatField(null=True,default=None)
	altitude = models.FloatField(null=True,default=None)
	ville = models.ForeignKey(Ville,on_delete=models.SET_NULL,null=True)

class Accident(models.Model):
	id_accident = models.AutoField(primary_key=True)
	time = models.DateTimeField(null=True,default=None)
	id_avion = models.ForeignKey(Avion, on_delete=models.SET_NULL,null=True)
	nom_compagnie = models.ForeignKey(Compagnie, on_delete=models.SET_NULL,null=True)
	nom_pays = models.ForeignKey(Pays, on_delete=models.SET_NULL,null=True)
	id_aeroport_depart = models.ForeignKey(Aeroport,related_name='depart',on_delete=models.SET_NULL,null=True)
	id_aeroport_arrivee = models.ForeignKey(Aeroport,related_name='arrivee',on_delete=models.SET_NULL,null=True)
	nb_occupants = models.IntegerField(null=True,default=None)
	nb_deces = models.IntegerField(null=True,default=None)
	emplacement = models.CharField(max_length=200,null=True,default=np.nan)
	phase_de_vol = models.CharField(max_length=200,null=True,default=np.nan)
	nature = models.CharField(max_length=200,null=True,default=np.nan)
	statut = models.CharField(max_length=200,null=True,default=np.nan)
	degats = models.CharField(max_length=200,null=True,default=np.nan)


	
