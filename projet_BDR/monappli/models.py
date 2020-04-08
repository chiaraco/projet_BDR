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
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=4)
	IdPays = models.ForeignKey(Pays, on_delete=models.CASCADE)
	 
class Pays(models.Model):
	NomPays = models.CharField(max_length=200,primary_key=True)

class Aeroport(models.Model):
	IdAeroport = models.AutoField(primary_key=True)
	NomAeroport = models.CharField(max_length=200)
	IATA = models.CharField(max_length=3)
	OACI = models.CharField(max_length=4)
	Latitude = FloatField()
	Longitude = FloatField()
	Altitude = FloatField()
	Ville = models.CharField(max_length=200)
	IdPays = models.ForeignKey(Pays, on_delete=models.CASCADE)

class Accident(models.Model):
	IdAccident = models.AutoField(primary_key=True)
	Time = DateTimeField()
	IdAvion = models.ForeignKey(Avion, on_delete=models.CASCADE)
	IdCompagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)
	IdPays = models.ForeignKey(Pays, on_delete=models.CASCADE)
	Aeroport_depart = models.ForeignKey(Aeroport, on_delete=models.CASCADE)
	Aeroport_arrivee = models.ForeignKey(Aeroport, on_delete=models.CASCADE)
	Nb_occupants = models.IntegerField()
	Nb_deces = models.IntegerField()
	Emplacement = models.CharField(max_length=200)
	Phase_de_vol = models.CharField(max_length=200)
	Nature = models.CharField(max_length=200)
	Statut = models.CharField(max_length=200)








	
