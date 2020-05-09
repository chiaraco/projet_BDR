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
accident=pd.read_csv('Donnees_accidents.csv',sep=';')



#### PAYS ####

pa_nan = Pays(nom_pays='Unknown')#, iso=np.nan
pa_nan.save()

for i in range(len(pays)) : 
	pa = Pays(nom_pays=pays.iloc[i][0], iso=pays.iloc[i][1])
	pa.save()



#### AVION ####
    
av_nan = Avion(modele='Unknown')#, iata=np.nan, oaci=np.nan)
av_nan.save()  

for k in range(len(avion)) : 
    av = Avion(modele=avion.iloc[k][0], iata=avion.iloc[k][1], oaci=avion.iloc[k][2])
    av.save()



#### AEROPORT ET VILLE ####
    
vi_nan = Ville(nom_ville='Unknown', nom_pays=pa_nan)
vi_nan.save()

ae_nan = Aeroport(nom_aeroport='Unknown',ville=vi_nan)#latitude=None, longitude=None, altitude=None,iata='', oaci='',
ae_nan.save() 

for l in range(len(aeroport)) :
	if pd.isnull(aeroport.iloc[l,1]) or aeroport.iloc[l,1]=="": # si pas de ville
		ae = Aeroport(nom_aeroport=aeroport.iloc[l,0], iata=aeroport.iloc[l,3], oaci=aeroport.iloc[l,4], latitude=aeroport.iloc[l,5], longitude=aeroport.iloc[l,6], altitude=aeroport.iloc[l,7], ville=vi_nan)
		ae.save() 

	else :
		try:
			pays=Pays.objects.get(nom_pays=aeroport.iloc[l,2])
		except ObjectDoesNotExist:
			print("ville",aeroport.iloc[l,2])
        
		try:   
			vi=Ville.objects.get(nom_ville=aeroport.iloc[l,1], nom_pays=pays)
		except ObjectDoesNotExist:
			vi = Ville(nom_ville=aeroport.iloc[l,1], nom_pays=pays)
			vi.save() 
        
		ae = Aeroport(nom_aeroport=aeroport.iloc[l,0], iata=aeroport.iloc[l,3], oaci=aeroport.iloc[l,4], latitude=aeroport.iloc[l,5], longitude=aeroport.iloc[l,6], altitude=aeroport.iloc[l,7], ville=vi)
		ae.save()           
    
    

#### COMPAGNIE ####
    
co_nan= Compagnie(nom_compagnie='Unknown', nom_pays=Pays.objects.get(nom_pays='Unknown'))#, alias='', iata='', oaci=''
co_nan.save()
    
for m in range(len(compagnie)) : 
	try:
		pa=Pays.objects.get(nom_pays=compagnie.iloc[m][4])
	except ObjectDoesNotExist:## Ce ne sont pas des pays
		pa=pa_nan
		            
	co = Compagnie(nom_compagnie=compagnie.iloc[m][0], alias=compagnie.iloc[m][1], iata=compagnie.iloc[m][2], oaci=compagnie.iloc[m][3], nom_pays=pa)
	co.save()  



#### ACCIDENT ####
    
import datetime
index_avion=[]
index_compagnie=[]
index_pays=[]
index_depart=[]
index_arrivee=[]
index_pas_de_date=[]

for n in range(len(accident)):
	try:
		modele_avion=Avion.objects.get(modele=accident.iloc[n][8])#elle existe, on ne fait rien de plus
	except ObjectDoesNotExist:
		if not pd.isnull(accident.iloc[n][8]):
			av = Avion(modele=accident.iloc[n][8])#, iata='', oaci=''
			av.save()
			modele_avion=av
		else:
			modele_avion=av_nan
		if not pd.isnull(accident.iloc[n][8]) and accident.iloc[n][8] not in index_avion:
			#print('modele_avion',n,accident.iloc[n][8])
			index_avion.append(accident.iloc[n][8])	
	
	try:
		compagnie=Compagnie.objects.get(nom_compagnie=accident.iloc[n][7])
	except ObjectDoesNotExist:
		if not pd.isnull(accident.iloc[n][7]):
			co = Compagnie(nom_compagnie=accident.iloc[n][7], nom_pays=pa_nan)#, alias='', iata='', oaci=''
			co.save()
			compagnie=co
		else:
			compagnie=co_nan
		if not pd.isnull(accident.iloc[n][7]) and accident.iloc[n][7] not in index_compagnie:
			index_compagnie.append(accident.iloc[n][7])
			#print('compagnie_accident',n,accident.iloc[n][7])
		

	try:
		pays=Pays.objects.get(nom_pays=accident.iloc[n][12])
	except ObjectDoesNotExist :
		if not pd.isnull(accident.iloc[n][12]):
			pa = Pays(nom_pays=accident.iloc[n][12])#, iso=''
			pa.save()
			pays=pa
		else:
			pays=pa_nan
		if not pd.isnull(accident.iloc[n][12]) and accident.iloc[n][12] not in index_pays:
			index_pays.append(accident.iloc[n][12])
			#print('pays_accident',n,accident.iloc[n][12])
		

	try:depart=Aeroport.objects.get(oaci=accident.iloc[n][15])
	except (ObjectDoesNotExist,MultipleObjectsReturned):

		try:depart=Aeroport.objects.get(iata=accident.iloc[n][17])
		except (ObjectDoesNotExist,MultipleObjectsReturned):

			try:depart=Aeroport.objects.get(nom_aeroport=accident.iloc[n][4])
			except (ObjectDoesNotExist,MultipleObjectsReturned):
				if not pd.isnull(accident.iloc[n][4]):
					ae = Aeroport(nom_aeroport=accident.iloc[n][4], ville=vi_nan)# latitude=0, longitude=0, altitude=0, iata='', oaci='',
					ae.save()
					depart=ae
				else:
					depart=ae_nan
				if not pd.isnull(accident.iloc[n][4]) and accident.iloc[n][4] not in index_depart:
					index_depart.append(accident.iloc[n][4])
					#print('aerodep_accident',n,accident.iloc[n][4])
								
					
#########
	try:arrivee=Aeroport.objects.get(oaci=accident.iloc[n][16])
	except (ObjectDoesNotExist,MultipleObjectsReturned):
		
		try:arrivee=Aeroport.objects.get(iata=accident.iloc[n][18])
		except (ObjectDoesNotExist,MultipleObjectsReturned):

			try:arrivee=Aeroport.objects.get(nom_aeroport=accident.iloc[n][5])
			except (ObjectDoesNotExist,MultipleObjectsReturned):
				if not pd.isnull(accident.iloc[n][5]):
					ae = Aeroport(nom_aeroport=accident.iloc[n][5],  ville=vi_nan)#latitude=0, longitude=0, altitude=0, iata='', oaci='',
					ae.save()
					arrivee=ae
				else:
					arrivee=ae_nan
				if not pd.isnull(accident.iloc[n][5]) and accident.iloc[n][5] not in index_arrivee:
					index_arrivee.append(accident.iloc[n][5])
					#print('aeroarr_accident',n,accident.iloc[n][5])

	degats=accident.iloc[n][9]
	if pd.isnull(accident.iloc[n][11]):nb_occupants=None
	else:nb_occupants=accident.iloc[n][11]
	if pd.isnull(accident.iloc[n][10]):Nb_deces=None
	else:Nb_deces=accident.iloc[n][10]
	emplacement=accident.iloc[n][0]
	phase_de_vol=accident.iloc[n][2]
	nature=accident.iloc[n][3]
	statut=accident.iloc[n][6]
	
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
	
	ac=Accident(time=T,id_avion=modele_avion,nom_compagnie=compagnie,nom_pays=pays,id_aeroport_depart=depart,id_aeroport_arrivee=arrivee,nb_occupants=nb_occupants,nb_deces=Nb_deces,emplacement=emplacement,phase_de_vol=phase_de_vol,nature=nature,statut=statut,degats=degats)
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
