#!/usr/bin/env python3
#-*- coding: utf-8 -*-

""" Peuplement des tables """

import pandas as pd
from monappli.models import Pays, Avion, Aeroport, Compagnie, Ville, Accident


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
	IdPays=ville.iloc[j][1]
	ligne_pays=pays.index[pays['Nom']==IdPays]
	pa=Pays(NomPays=pays.iloc[ligne_pays][0], ISO=pays.iloc[ligne_pays][1])
    vi = Ville(NomVille=ville.iloc[j][0], NomPays=pa)
    vi.save()
  
    
for k in range(len(avion)) : 
    av = Avion(Modele=avion.iloc[k][0], IATA=avion.iloc[k][1], OACI=avion.iloc[k][2])
    av.save()
    

for l in range(len(aeroport)) : 
	IdVille=aeroport.iloc[l][1]
	ligne_ville=aeroport.index[aeroport['Ville']==IdVille]

	IdPays=ville.iloc[ligne_ville][1]
	ligne_pays=pays.index[pays['Nom']==IdPays]
	pa=Pays(NomPays=pays.iloc[ligne_pays][0], ISO=pays.iloc[ligne_pays][1])
	
	vi=Ville(NomVille=ville.iloc[ligne_ville][0], NomPays=pa)
    ae = Aeroport(NomAeroport=aeroport.iloc[l][0], IATA=aeroport.iloc[l][3], OACI=aeroport.iloc[l][4], Latitude=aeroport.iloc[l][5], Longitude=aeroport.iloc[l][6], Altitude=aeroport.iloc[l][7], Ville=vi)
    ae.save()   
    
    
for m in range(len(compagnie)) : 
	IdPays=pays.iloc[m][1]
	ligne_pays=pays.index[pays['Nom']==IdPays]
	pa=Pays(NomPays=pays.iloc[ligne_pays][0], ISO=pays.iloc[ligne_pays][1])

    co = Compagnie(NomCompagnie=compagnie.iloc[m][0], Alias=compagnie.iloc[m][1], IATA=compagnie.iloc[m][2], OACI=compagnie.iloc[m][3], NomPays=compagnie.iloc[m][4])
    co.save()  

import datetime
index_avion=[]
index_compagnie=[]
index_pays=[]
index_depart=[]
index_arrivee=[]
for n in range(len(accident)):
	IdAvion=accident.iloc[n][8]
	if IdAvion not in avion[0]:
		index_avion.append(n)
	else :
		ligne_avion=avion.index[avion['Modele']==IdAvion]
		av=Avion(Modele=avion.iloc[ligne_avion][0], IATA=avion.iloc[ligne_avion][1], OACI=avion.iloc[ligne_avion][2])
	
	IdCompagnie=accident.iloc[n][7]
	if IdCompagnie not in compagnie[0]:
		index_compagnie.append(n)
	else :
		ligne_compagnie=compagnie.index[compagnie['Compagnie']==IdCompagnie]
		co=Compagnie(NomCompagnie=compagnie.iloc[ligne_compagnie][0], Alias=compagnie.iloc[ligne_compagnie][1], IATA=compagnie.iloc[ligne_compagnie][2], OACI=compagnie.iloc[ligne_compagnie][3], NomPays=compagnie.iloc[ligne_compagnie][4])

	IdPays=accident.iloc[n][12]
	if IdPays not in pays[0]:
		index_pays.append(n)
	else :
		ligne_pays=pays.index[pays['Pays']==IdPays]
		pa=Pays(NomPays=pays.iloc[ligne_pays][0], ISO=pays.iloc[ligne_pays][1])

	IdAeroport_depart=accident.iloc[n][4]
	OACI_depart=accident.iloc[n][15]
	IATA_depart=accident.iloc[n][17]
	if OACI_depart not in aeroport[3]:
		if IATA_depart not in aeroport[2]:
			if IdAeroport_depart not in aeroport[0]:
				index_depart.append(n)
			else:
				ligne_depart=aeroport.index[aeroport['Nom']==IdAeroport_depart]
				ae = Aeroport(NomAeroport=aeroport.iloc[ligne_depart][0], IATA=aeroport.iloc[ligne_depart][3], OACI=aeroport.iloc[ligne_depart][4], Latitude=aeroport.iloc[ligne_depart][5], Longitude=aeroport.iloc[ligne_depart][6], Altitude=aeroport.iloc[ligne_depart][7], Ville=aeroport.iloc[ligne_depart][1])
		
		else :
			ligne_depart=aeroport.index[aeroport['IATA']==IATA_depart]
			ae = Aeroport(NomAeroport=aeroport.iloc[ligne_depart][0], IATA=aeroport.iloc[ligne_depart][3], OACI=aeroport.iloc[ligne_depart][4], Latitude=aeroport.iloc[ligne_depart][5], Longitude=aeroport.iloc[ligne_depart][6], Altitude=aeroport.iloc[ligne_depart][7], Ville=aeroport.iloc[ligne_depart][1])


	else:
		ligne_depart=aeroport.index[aeroport['OACI']==OACI_depart]
		ae = Aeroport(NomAeroport=aeroport.iloc[ligne_depart][0], IATA=aeroport.iloc[ligne_depart][3], OACI=aeroport.iloc[ligne_depart][4], Latitude=aeroport.iloc[ligne_depart][5], Longitude=aeroport.iloc[ligne_depart][6], Altitude=aeroport.iloc[ligne_depart][7], Ville=aeroport.iloc[ligne_depart][1])

#########
	IdAeroport_arrivee=accident.iloc[n][5]
	OACI_arrivee=accident.iloc[n][16]
	IATA_arrivee=accident.iloc[n][18]
	if OACI_arrivee not in aeroport[3]:
		if IATA_arrivee not in aeroport[2]:
			if IdAeroport_arrivee not in aeroport[0]:
				index_arrivee.append(n)
			else:
				ligne_arrivee=aeroport.index[aeroport['Nom']==IdAeroport_arrivee]
				ae = Aeroport(NomAeroport=aeroport.iloc[ligne_arrivee][0], IATA=aeroport.iloc[ligne_arrivee][3], OACI=aeroport.iloc[ligne_arrivee][4], Latitude=aeroport.iloc[ligne_arrivee][5], Longitude=aeroport.iloc[ligne_arrivee][6], Altitude=aeroport.iloc[ligne_arrivee][7], Ville=aeroport.iloc[ligne_arrivee][1])
		
		else :
			ligne_arrivee=aeroport.index[aeroport['IATA']==IATA_arrivee]
			ae = Aeroport(NomAeroport=aeroport.iloc[ligne_arrivee][0], IATA=aeroport.iloc[ligne_arrivee][3], OACI=aeroport.iloc[ligne_arrivee][4], Latitude=aeroport.iloc[ligne_arrivee][5], Longitude=aeroport.iloc[ligne_arrivee][6], Altitude=aeroport.iloc[ligne_arrivee][7], Ville=aeroport.iloc[ligne_arrivee][1])


	else:
		ligne_arrivee=aeroport.index[aeroport['OACI']==OACI_arrivee]
		ae = Aeroport(NomAeroport=aeroport.iloc[ligne_arrivee][0], IATA=aeroport.iloc[ligne_arrivee][3], OACI=aeroport.iloc[ligne_arrivee][4], Latitude=aeroport.iloc[ligne_arrivee][5], Longitude=aeroport.iloc[ligne_arrivee][6], Altitude=aeroport.iloc[ligne_arrivee][7], Ville=aeroport.iloc[ligne_arrivee][1])



	Degats=accident.iloc[n][9]
	Nb_occupants=int(accident.iloc[n][11])
	Nb_deces=int(accident.iloc[n][10])
	Emplacement=accident.iloc[n][0]
	Phase_de_vol=accident.iloc[n][2]
	Nature=accident.iloc[n][3]
	Statut=accident.iloc[n][6]
	date=datetime(year=int(accident.iloc[n][22]),month=int(accident.iloc[n][21]),day=int(accident.iloc[n][20]),hour=int(accident.iloc[n][1]),minute=int(accident.iloc[n][19]))
	
	ac=Accident()
	ac.save()
    
