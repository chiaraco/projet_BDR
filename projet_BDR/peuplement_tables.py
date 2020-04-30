#!/usr/bin/env python3
#-*- coding: utf-8 -*-

""" Peuplement des tables """

import pandas as pd
from monappli.models import Pays, Avion, Aeroport, Compagnie, Ville, Accident
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import numpy as np

pays=pd.read_csv('pays.csv',sep=';')
avion=pd.read_csv('avion.csv',sep=';')
aeroport=pd.read_csv('aeroport.csv',sep=';')
compagnie=pd.read_csv('compagnie.csv',sep=';')
ville=pd.read_csv('ville.csv',sep=';')
accident=pd.read_csv('Donnees_accidents.csv',sep=';')


for i in range(len(pays)) : 
    pa = Pays(NomPays=pays.iloc[i][0], ISO=pays.iloc[i][1])
    pa.save()


for j in range(len(ville)) :
	try:
		pays=Pays.objects.get(NomPays=ville.iloc[j][1])
	except ObjectDoesNotExist:
		print("ville",ville.iloc[j][1])
	vi = Ville(NomVille=ville.iloc[j][0], NomPays=pays)
	vi.save()
  
    
for k in range(len(avion)) : 
    av = Avion(Modele=avion.iloc[k][0], IATA=avion.iloc[k][1], OACI=avion.iloc[k][2])
    av.save()
    

for l in range(len(aeroport)) : 
	try :
		ville=Ville.objects.get(NomVille=aeroport.iloc[l][1])
	except ObjectDoesNotExist:
		print("aeroport",aeroport.iloc[l][1])
	ae = Aeroport(NomAeroport=aeroport.iloc[l][0], IATA=aeroport.iloc[l][2], OACI=aeroport.iloc[l][3], Latitude=aeroport.iloc[l][4], Longitude=aeroport.iloc[l][5], Altitude=aeroport.iloc[l][6], Ville=ville)
	ae.save()   
    
compt=0
compagnie_nan=[]    
for m in range(len(compagnie)) : 
	try:
		pa=Pays.objects.get(NomPays=compagnie.iloc[m][4])
	except ObjectDoesNotExist:
		if pd.isnull(compagnie.iloc[m][4]):
			compagnie_nan.append(m)
		print("compagnie",compagnie.iloc[m][4],m)
		compt+=1
	co = Compagnie(NomCompagnie=compagnie.iloc[m][0], Alias=compagnie.iloc[m][1], IATA=compagnie.iloc[m][2], OACI=compagnie.iloc[m][3], NomPays=pa)
	co.save()  
print("Nombre de pays non trouvés dans compagnie:",compt)
print("liste des nan trouvés dans compagnie:",compagnie_nan)


import datetime
index_avion=[]
index_compagnie=[]
index_pays=[]
index_depart=[]
index_arrivee=[]
save=True
for n in range(len(accident)):
	try:
		modele_avion=Avion.objects.get(Modele=accident.iloc[n][8])#elle existe, on ne fait rien de plus
	except ObjectDoesNotExist:
		print('modele_avion',n,accident.iloc[n][8])
		index_avion.append(n)
		save=False
	
	try:
		compagnie=Compagnie.objects.get(NomCompagnie=accident.iloc[n][7])
	except ObjectDoesNotExist:
		index_compagnie.append(n)
		save=False

	try:
		pays=Pays.objects.get(NomPays=accident.iloc[n][12])
	except ObjectDoesNotExist :
		index_pays.append(n)
		save=False

	try:depart=Aeroport.objects.get(OACI=accident.iloc[n][15])
	except (ObjectDoesNotExist,MultipleObjectsReturned):

		try:depart=Aeroport.objects.get(IATA=accident.iloc[n][17])
		except (ObjectDoesNotExist,MultipleObjectsReturned):

			try:depart=Aeroport.objects.get(NomAeroport=accident.iloc[n][4])
			except (ObjectDoesNotExist,MultipleObjectsReturned):
				index_depart.append(n)
				save=False
				
					
#########
	try:arrivee=Aeroport.objects.get(OACI=accident.iloc[n][16])
	except (ObjectDoesNotExist,MultipleObjectsReturned):
		
		try:arrivee=Aeroport.objects.get(IATA=accident.iloc[n][18])
		except (ObjectDoesNotExist,MultipleObjectsReturned):

			try:arrivee=Aeroport.objects.get(NomAeroport=accident.iloc[n][5])
			except (ObjectDoesNotExist,MultipleObjectsReturned):
				index_arrivee.append(n)
				save=False

	Degats=accident.iloc[n][9]
	if pd.isnull(accident.iloc[n][11]):Nb_occupants=''
	else:Nb_occupants=int(accident.iloc[n][11])
	if pd.isnull(accident.iloc[n][10]):Nb_deces=''
	else:Nb_deces=int(accident.iloc[n][10])
	Emplacement=accident.iloc[n][0]
	Phase_de_vol=accident.iloc[n][2]
	Nature=accident.iloc[n][3]
	Statut=accident.iloc[n][6]
	
## Date	
	
	if pd.isnull(accident.iloc[n][19]):#minutes
		if pd.isnull(accident.iloc[n][1]):#heure
			if pd.isnull(accident.iloc[n][20]):#jour
				if pd.isnull(accident.iloc[n][21]):#mois
					if pd.isnull(accident.iloc[n][22]):#annee
						print("pas de date")
						
					else:
						T=datetime.datetime(year=int(accident.iloc[n][22]),month=1,day=1)
				else:
					T=datetime.datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=1)
			else:
				T=datetime.datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=int(accident.iloc[n][20]))	
		else:
			T=datetime.datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=int(accident.iloc[n][20]),hour=int(accident.iloc[n][1]),minute=0)
	else:
		T=datetime.datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=int(accident.iloc[n][20]),hour=int(accident.iloc[n][1]),minute=int(accident.iloc[n][19]))




#	T=datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=int(accident.iloc[n][20]),hour=int(accident.iloc[n][1]),minute=int(accident.iloc[n][19]))
	
	if save:
		ac=Accident(Time=T,IdAvion=modele_avion,NomCompagnie=compagnie,NomPays=pays,IdAeroport_depart=depart,IdAeroport_arrivee=arrivee,Nb_occupant=Nb_occupant,Nb_deces=Nb_deces,Emplacement=Emplacement,Pase_de_vol=Pase_de_vol,Nature=Nature,Statut=Statut,Degats=Degats)
		ac.save()
print("index_avion",index_avion)
print("index_compagnie",index_compagnie)
print("index_pays",index_pays)
print("index_depart",index_depart)
print("index_arrivee",index_arrivee)
