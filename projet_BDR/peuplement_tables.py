#!/usr/bin/env python3
#-*- coding: utf-8 -*-

""" Peuplement des tables """

import pandas as pd
from monappli.models import Pays, Avion, Aeroport, Compagnie, Ville, Accident
from django.core.exceptions import ObjectDoesNotExist


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
		print(ville.iloc[j][1])
	vi = Ville(NomVille=ville.iloc[j][0], NomPays=pays)
	vi.save()
  
    
for k in range(len(avion)) : 
    av = Avion(Modele=avion.iloc[k][0], IATA=avion.iloc[k][1], OACI=avion.iloc[k][2])
    av.save()
    

for l in range(len(aeroport)) : 
	try :
		ville=Ville.objects.get(NomVille=aeroport.iloc[l][1])
	except ObjectDoesNotExist:
		print(aeroport.iloc[l][1])
	ae = Aeroport(NomAeroport=aeroport.iloc[l][0], IATA=aeroport.iloc[l][2], OACI=aeroport.iloc[l][3], Latitude=aeroport.iloc[l][4], Longitude=aeroport.iloc[l][5], Altitude=aeroport.iloc[l][6], Ville=ville)
	ae.save()   
    
    
for m in range(len(compagnie)) : 
	try:
		pa=Pays.objects.get(NomPays=compagnie.iloc[m][4])
	except ObjectDoesNotExist:
		print("compagnie",compagnie.iloc[m][4],m)
	co = Compagnie(NomCompagnie=compagnie.iloc[m][0], Alias=compagnie.iloc[m][1], IATA=compagnie.iloc[m][2], OACI=compagnie.iloc[m][3], NomPays=pa)
	co.save()  

import datetime
index_avion=[]
index_compagnie=[]
index_pays=[]
index_depart=[]
index_arrivee=[]
for n in range(len(accident)):
	try:
		modele=Avion.objects.get(Modele=accident.iloc[n][8])#elle existe, on ne fait rien de plus
	except ObjectDoesNotExist as err:
		index_avion.append(n)
		
	
	try:
		compagnie=Compagnie.objects.get(NomCompagnie=accident.iloc[n][7])
	except ObjectDoesNotExist as err:
		index_compagnie.append(n)

	try:
		pays=Pays.objects.get(NomPays=accident.iloc[n][12])
	except ObjectDoesNotExist as err:
		index_pays.append(n)

	try:depart=Aeroport.objects.get(OACI=accident.iloc[n][15])
	except ObjectDoesNotExist as err:

		try:depart=Aeroport.objects.get(IATA=accident.iloc[n][17])
		except ObjectDoesNotExist as err:

			try:depart=Aeroport.objects.get(NomAeroport=accident.iloc[n][4])
			except ObjectDoesNotExist as err:index_depart.append(n)
					
#########
	try:arrivee=Aeroport.objects.get(OACI=accident.iloc[n][16])
	except ObjectDoesNotExist as err:

		try:arrivee=Aeroport.objects.get(IATA=accident.iloc[n][18])
		except ObjectDoesNotExist as err:

			try:arrivee=Aeroport.objects.get(NomAeroport=accident.iloc[n][5])
			except ObjectDoesNotExist as err:index_arrivee.append(n)

	Degats=accident.iloc[n][9]
	Nb_occupants=int(accident.iloc[n][11])
	Nb_deces=int(accident.iloc[n][10])
	Emplacement=accident.iloc[n][0]
	Phase_de_vol=accident.iloc[n][2]
	Nature=accident.iloc[n][3]
	Statut=accident.iloc[n][6]
	date=datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=int(accident.iloc[n][20]),hour=int(accident.iloc[n][1]),minute=int(accident.iloc[n][19]))
	
	ac=Accident(Time=date,IdAvion=modele,NomCompagnie=compagnie,NomPays=pays,IdAeroport_depart=depart,IdAeroport_arrivee=arrivee,Nb_occupant=Nb_occupant,Nb_deces=Nb_deces,Emplacement=Emplacement,Pase_de_vol=Pase_de_vol,Nature=Nature,Statut=Statut,Degats=Degats)
	ac.save()
    
