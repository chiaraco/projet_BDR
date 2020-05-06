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

pa = Pays(NomPays='Unknown', ISO='')
pa.save()
for i in range(len(pays)) : 
	pa = Pays(NomPays=pays.iloc[i][0], ISO=pays.iloc[i][1])
	pa.save()

vi = Ville(NomVille='Unknown', NomPays=Pays.objects.get(NomPays='Unknown'))
vi.save()
for j in range(len(ville)) :
	try:
		pays=Pays.objects.get(NomPays=ville.iloc[j][1])
	except ObjectDoesNotExist:
		print("ville",ville.iloc[j][1])
	vi = Ville(NomVille=ville.iloc[j][0], NomPays=pays)
	vi.save()
  
av = Avion(Modele='Unknown', IATA='', OACI='')
av.save()  
for k in range(len(avion)) : 
    av = Avion(Modele=avion.iloc[k][0], IATA=avion.iloc[k][1], OACI=avion.iloc[k][2])
    av.save()
    
ae = Aeroport(NomAeroport='Unknown', IATA='', OACI='',  Ville=Ville.objects.get(NomVille='Unknown'))#Latitude=None, Longitude=None, Altitude=None,
ae.save()  
for l in range(len(aeroport)) : 
	try :
		ville=Ville.objects.get(NomVille=aeroport.iloc[l][1])
	except ObjectDoesNotExist:
		print("aeroport",aeroport.iloc[l][1])
	ae = Aeroport(NomAeroport=aeroport.iloc[l][0], IATA=aeroport.iloc[l][2], OACI=aeroport.iloc[l][3], Latitude=aeroport.iloc[l][4], Longitude=aeroport.iloc[l][5], Altitude=aeroport.iloc[l][6], Ville=ville)
	ae.save()   
    
 
co = Compagnie(NomCompagnie='Unknown', Alias='', IATA='', OACI='', NomPays=Pays.objects.get(NomPays='Unknown'))
co.save()     
for m in range(len(compagnie)) : 
	try:
		pa=Pays.objects.get(NomPays=compagnie.iloc[m][4])
	except ObjectDoesNotExist:
		if not pd.isnull(compagnie.iloc[m][4]):
			print("compagnie",compagnie.iloc[m][4],m)
	co = Compagnie(NomCompagnie=compagnie.iloc[m][0], Alias=compagnie.iloc[m][1], IATA=compagnie.iloc[m][2], OACI=compagnie.iloc[m][3], NomPays=pa)
	co.save()  


import datetime
index_avion=[]
index_compagnie=[]
index_pays=[]
index_depart=[]
index_arrivee=[]
index_pas_de_date=[]
for n in range(1200,1500):
	try:
		modele_avion=Avion.objects.get(Modele=accident.iloc[n][8])#elle existe, on ne fait rien de plus
	except ObjectDoesNotExist:
		if not pd.isnull(accident.iloc[n][8]):
			av = Avion(Modele=accident.iloc[n][8], IATA='', OACI='')
			av.save()
			modele_avion=av
		else:
			modele_avion=Avion.objects.get(Modele='Unknown')
		if not pd.isnull(accident.iloc[n][8]) and accident.iloc[n][8] not in index_avion:
			#print('modele_avion',n,accident.iloc[n][8])
			index_avion.append(accident.iloc[n][8])	
	
	try:
		compagnie=Compagnie.objects.get(NomCompagnie=accident.iloc[n][7])
	except ObjectDoesNotExist:
		if not pd.isnull(accident.iloc[n][7]):
			co = Compagnie(NomCompagnie=accident.iloc[n][7], Alias='', IATA='', OACI='', NomPays=Pays.objects.get(NomPays='Unknown'))
			co.save()
			compagnie=co
		else:
			compagnie=Compagnie.objects.get(NomCompagnie='Unknown')
		if not pd.isnull(accident.iloc[n][7]) and accident.iloc[n][7] not in index_compagnie:
			index_compagnie.append(accident.iloc[n][7])
			#print('compagnie_accident',n,accident.iloc[n][7])
		

	try:
		pays=Pays.objects.get(NomPays=accident.iloc[n][12])
	except ObjectDoesNotExist :
		if not pd.isnull(accident.iloc[n][12]):
			pa = Pays(NomPays=accident.iloc[n][12], ISO='')
			pa.save()
			pays=pa
		else:
			pays=Pays.objects.get(NomPays='Unknown')
		if not pd.isnull(accident.iloc[n][12]) and accident.iloc[n][12] not in index_pays:
			index_pays.append(accident.iloc[n][12])
			#print('pays_accident',n,accident.iloc[n][12])
		

	try:depart=Aeroport.objects.get(OACI=accident.iloc[n][15])
	except (ObjectDoesNotExist,MultipleObjectsReturned):

		try:depart=Aeroport.objects.get(IATA=accident.iloc[n][17])
		except (ObjectDoesNotExist,MultipleObjectsReturned):

			try:depart=Aeroport.objects.get(NomAeroport=accident.iloc[n][4])
			except (ObjectDoesNotExist,MultipleObjectsReturned):
				if not pd.isnull(accident.iloc[n][4]):
					ae = Aeroport(NomAeroport=accident.iloc[n][4], IATA='', OACI='', Ville=Ville.objects.get(NomVille='Unknown'))# Latitude=0, Longitude=0, Altitude=0,
					ae.save()
					depart=ae
				else:
					depart=Aeroport.objects.get(NomAeroport='Unknown')
				if not pd.isnull(accident.iloc[n][4]) and accident.iloc[n][4] not in index_depart:
					index_depart.append(accident.iloc[n][4])
					#print('aerodep_accident',n,accident.iloc[n][4])
								
					
#########
	try:arrivee=Aeroport.objects.get(OACI=accident.iloc[n][16])
	except (ObjectDoesNotExist,MultipleObjectsReturned):
		
		try:arrivee=Aeroport.objects.get(IATA=accident.iloc[n][18])
		except (ObjectDoesNotExist,MultipleObjectsReturned):

			try:arrivee=Aeroport.objects.get(NomAeroport=accident.iloc[n][5])
			except (ObjectDoesNotExist,MultipleObjectsReturned):
				if not pd.isnull(accident.iloc[n][5]):
					ae = Aeroport(NomAeroport=accident.iloc[n][5], IATA='', OACI='',  Ville=Ville.objects.get(NomVille='Unknown'))#Latitude=0, Longitude=0, Altitude=0,
					ae.save()
					arrivee=ae
				else:
					arrivee=Aeroport.objects.get(NomAeroport='Unknown')
				if not pd.isnull(accident.iloc[n][5]) and accident.iloc[n][5] not in index_arrivee:
					index_arrivee.append(accident.iloc[n][5])
					#print('aeroarr_accident',n,accident.iloc[n][5])

	Degats=accident.iloc[n][9]
	if pd.isnull(accident.iloc[n][11]):Nb_occupants=None
	else:Nb_occupants=accident.iloc[n][11]
	if pd.isnull(accident.iloc[n][10]):Nb_deces=None
	else:Nb_deces=accident.iloc[n][10]
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
						index_pas_de_date.append(n)
						
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
	
	ac=Accident(Time=T,IdAvion=modele_avion,NomCompagnie=compagnie,NomPays=pays,IdAeroport_depart=depart,IdAeroport_arrivee=arrivee,Nb_occupants=Nb_occupants,nb_deces=Nb_deces,Emplacement=Emplacement,Phase_de_vol=Phase_de_vol,Nature=Nature,Statut=Statut,Degats=Degats)
	ac.save()
print("index_avion",index_avion)
print("index_compagnie",index_compagnie)
print("index_depart",index_depart)
print("index_arrivee",index_arrivee)
print("index_pays",index_pays)
print("index_pas_de_date",index_pas_de_date)
print("index_avion:",len(index_avion),"index_compagnie:",len(index_compagnie),"index_pays",len(index_pays),"index_depart",len(index_depart),"index_arrivee",len(index_arrivee))

import csv

with open('index_avion.csv', 'w',encoding='utf-8',newline='') as csvfile:#newline evite d'avoir un saut de ligne entre chaque ligne
	spamwriter = csv.writer(csvfile, delimiter=';')
	for i in index_avion:
		spamwriter.writerow(i)

with open('index_compagnie.csv', 'w',encoding='utf-8',newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=';')
	for i in index_compagnie:
		spamwriter.writerow(i)

with open('index_depart.csv', 'w',encoding='utf-8',newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=';')
	for i in index_depart:
		spamwriter.writerow(i)

with open('index_arrivee.csv', 'w',encoding='utf-8',newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=';')
	for i in index_arrivee:
		spamwriter.writerow(i)
