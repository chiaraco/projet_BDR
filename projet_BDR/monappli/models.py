from django.db import models

# Create your models here.

class Avion(models.Model):
	IdAvion =  models.AutoField(primary_key=True)
	Modele = models.CharField(max_length=200)
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=4)
	
class Compagnie(models.Model):
	NomCompagnie = models.CharField(max_length=200,primary_key=True)
	Alias = models.CharField(max_length=10)
	IATA = models.CharField(max_length=2)
	OACI = models.CharField(max_length=3)
	NomPays = models.ForeignKey(Pays, on_delete=models.CASCADE)
	 
class Pays(models.Model):
	NomPays = models.CharField(max_length=200,primary_key=True)
	ISO = models.CharField(max_length=2)

class Aeroport(models.Model):
	IdAeroport = models.AutoField(primary_key=True)
	NomAeroport = models.CharField(max_length=200)
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=4)
	Latitude = models.FloatField()
	Longitude = models.FloatField()
	Altitude = models.FloatField()
	Ville = models.CharField(max_length=200)
	NomPays = models.ForeignKey(Pays, on_delete=models.CASCADE)

class Accident(models.Model):
	IdAccident = models.AutoField(primary_key=True)
	Time = models.DateTimeField()
	IdAvion = models.ForeignKey(Avion, on_delete=models.CASCADE)
	NomCompagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)
	NomPays = models.ForeignKey(Pays, on_delete=models.CASCADE)
	IdAeroport_depart = models.ForeignKey(Aeroport, on_delete=models.CASCADE)
	IdAeroport_arrivee = models.ForeignKey(Aeroport, on_delete=models.CASCADE)
	Nb_occupants = models.IntegerField()
	Nb_deces = models.IntegerField()
	Emplacement = models.CharField(max_length=200)
	Phase_de_vol = models.CharField(max_length=200)
	Nature = models.CharField(max_length=200)
	Statut = models.CharField(max_length=200)








	
