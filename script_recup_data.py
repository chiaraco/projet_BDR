#!/usr/bin/env python3
#-*- coding: utf-8 -*-



""" Récupération des données du site https://openflights.org/data.html """

# on récupère seulement les colonnes qui nous intéressent
# et on les mémorise dans des dataframe


import pandas as pd


col_pays=["Pays","ISO"]
pays=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat", delimiter=",", names=col_pays, usecols=[0,1])
#print(pays)


col_avion=["Modele","IATA","OACI"]
avion=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/planes.dat", delimiter=",", names=col_avion, usecols=[0,1,2])
#print(avion)


col_aeroport=["Nom","Ville","Pays","IATA","OACI","Lat","Lon","Alt"]
aeroport=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat", delimiter=",", names=col_aeroport, usecols=[1,2,3,4,5,6,7,8])
#print(aeroport)


col_compagnie=["Nom","Alias","IATA","OACI","Pays"]
compagnie=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat", delimiter=",", names=col_compagnie, usecols=[1,2,3,4,6])
#print(compagnie)



""" Création des tables correspondantes """


# on parcourt chacun des dataframe pour peupler les tables


from monappli.models import Pays, Avion, Aeroport, Compagnie


for i in range(len(pays)) : 
    pa = Pays(NomPays=pays.iloc[i][0], ISO=pays.iloc[i][1])
    pa.save
    
  
for j in range(len(avion)) : 
    av = Avion(Modele=avion.iloc[j][0], IATA=avion.iloc[j][1], OACI=avion.iloc[j][2])
    av.save
    

for k in range(len(aeroport)) : 
    ae = Aeroport(NomAeroport=aeroport.iloc[k][0], IATA=aeroport.iloc[k][3], OACI=aeroport.iloc[k][4], Latitude=aeroport.iloc[k][5], Longitude=aeroport.iloc[k][6], Altitude=aeroport.iloc[k][7], Ville=aeroport.iloc[k][1], NomPays=aeroport.iloc[k][2])
    ae.save   
    
    
for l in range(len(compagnie)) : 
    co = Compagnie(NomCompagnie=compagnie.iloc[l][0], Alias=compagnie.iloc[l][1], IATA=compagnie.iloc[l][2], OACI=compagnie.iloc[l][3], NomPays=compagnie.iloc[l][4])
    co.save  
    
    
    
    
    
    
    
    
    
    
    