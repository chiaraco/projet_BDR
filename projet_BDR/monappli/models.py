from django.db import models

# Create your models here.
class Pays(models.Model):
	NomPays = models.CharField(max_length=200,primary_key=True)
	ISO = models.CharField(max_length=3)

class Avion(models.Model):
	IdAvion =  models.AutoField(primary_key=True)
	Modele = models.CharField(max_length=200)
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=4)
	
class Compagnie(models.Model):
	NomCompagnie = models.CharField(max_length=200,primary_key=True)
	Alias = models.CharField(max_length=30)
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=3)
	NomPays = models.ForeignKey(Pays, on_delete=models.SET_NULL,null=True)

class Ville(models.Model):
	NomVille = models.CharField(max_length=200,primary_key=True)
	NomPays = models.ForeignKey(Pays, on_delete=models.SET_NULL,null=True)

class Aeroport(models.Model):
	IdAeroport = models.AutoField(primary_key=True)
	NomAeroport = models.CharField(max_length=200)
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=4)
	Latitude = models.FloatField(null=True,default=None)
	Longitude = models.FloatField(null=True,default=None)
	Altitude = models.FloatField(null=True,default=None)
	Ville = models.ForeignKey(Ville,on_delete=models.SET_NULL,null=True)

class Accident(models.Model):
	IdAccident = models.AutoField(primary_key=True)
	Time = models.DateTimeField(null=True,default=None)
	IdAvion = models.ForeignKey(Avion, on_delete=models.SET_NULL,null=True)
	NomCompagnie = models.ForeignKey(Compagnie, on_delete=models.SET_NULL,null=True)
	NomPays = models.ForeignKey(Pays, on_delete=models.SET_NULL,null=True)
	IdAeroport_depart = models.ForeignKey(Aeroport,related_name='depart',on_delete=models.SET_NULL,null=True)
	IdAeroport_arrivee = models.ForeignKey(Aeroport,related_name='arrivee',on_delete=models.SET_NULL,null=True)
	Nb_occupants = models.IntegerField(null=True,default=None)
	nb_deces = models.IntegerField(null=True,default=None)
	Emplacement = models.CharField(max_length=200)
	Phase_de_vol = models.CharField(max_length=200)
	Nature = models.CharField(max_length=200)
	Statut = models.CharField(max_length=200)
	Degats = models.CharField(max_length=200)


	
