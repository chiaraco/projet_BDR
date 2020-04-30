from django.db import models

# Create your models here.
class Pays(models.Model):
	NomPays = models.CharField(max_length=200,primary_key=True)
	ISO = models.CharField(max_length=3, blank=True,null=True,unique=True)

class Avion(models.Model):
	IdAvion =  models.AutoField(primary_key=True)
	Modele = models.CharField(max_length=200, blank=True)
	IATA = models.CharField(max_length=3, blank=True,null=True,unique=True)
	OACI = models.CharField(max_length=4, blank=True,null=True,unique=True)
	
class Compagnie(models.Model):
	NomCompagnie = models.CharField(max_length=200,primary_key=True)
	Alias = models.CharField(max_length=30, blank=True)
	IATA = models.CharField(max_length=3, blank=True,null=True,unique=True)
	OACI = models.CharField(max_length=3, blank=True,null=True,unique=True)
	NomPays = models.ForeignKey(Pays, on_delete=models.CASCADE,blank=True,null=True)

class Ville(models.Model):
	NomVille = models.CharField(max_length=200,primary_key=True)
	NomPays = models.ForeignKey(Pays, on_delete=models.CASCADE)

class Aeroport(models.Model):
	IdAeroport = models.AutoField(primary_key=True)
	NomAeroport = models.CharField(max_length=200, blank=True)
	IATA = models.CharField(max_length=3, blank=True,unique=True,null=True)
	OACI = models.CharField(max_length=4, blank=True,unique=True,null=True)
	Latitude = models.FloatField(blank=True)
	Longitude = models.FloatField(blank=True)
	Altitude = models.FloatField(blank=True)
	Ville = models.ForeignKey(Ville,on_delete=models.CASCADE)

class Accident(models.Model):
	IdAccident = models.AutoField(primary_key=True)
	Time = models.DateTimeField(blank=True)
	IdAvion = models.ForeignKey(Avion, on_delete=models.SET_NULL,blank=True,null=True)
	NomCompagnie = models.ForeignKey(Compagnie, on_delete=models.SET_NULL,blank=True,null=True)
	NomPays = models.ForeignKey(Pays, on_delete=models.SET_NULL,blank=True,null=True)
	IdAeroport_depart = models.ForeignKey(Aeroport,related_name='depart',on_delete=models.CASCADE, default=None,blank=True)
	IdAeroport_arrivee = models.ForeignKey(Aeroport,related_name='arrivee',on_delete=models.CASCADE,default=None,blank=True)
	Nb_occupants = models.IntegerField(blank=True)
	Nb_deces = models.IntegerField(blank=True)
	Emplacement = models.CharField(max_length=200, blank=True)
	Phase_de_vol = models.CharField(max_length=200, blank=True)
	Nature = models.CharField(max_length=200, blank=True)
	Statut = models.CharField(max_length=200, blank=True)
	Degats = models.CharField(max_length=200, blank=True)








	
