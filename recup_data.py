#!/usr/bin/env python3
#-*- coding: utf-8 -*-



""" Récupération des données du site https://openflights.org/data.html """

# on récupère seulement les colonnes qui nous intéressent
# et on les mémorise dans des dataframe


import pandas as pd


col_pays=["Pays","ISO"]
pays=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat", delimiter=",", names=col_pays, usecols=[0,1])
#print(pays)
pays.to_csv(r'C:\Users\cordi\Documents\projet_BDR\pays.csv',sep=';',index=False)


col_avion=["Modele","IATA","OACI"]
avion=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/planes.dat", delimiter=",", names=col_avion, usecols=[0,1,2])
#print(avion)
avion.to_csv(r'C:\Users\cordi\Documents\projet_BDR\avion.csv',sep=';',index=False)


col_aeroport=["Nom","Ville","Pays","IATA","OACI","Lat","Lon","Alt"]
aeroport=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat", delimiter=",", names=col_aeroport, usecols=[1,2,3,4,5,6,7,8])
#print(aeroport)
aeroport.to_csv(r'C:\Users\cordi\Documents\projet_BDR\aeroport.csv',sep=';',index=False)


col_compagnie=["Nom","Alias","IATA","OACI","Pays"]
compagnie=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat", delimiter=",", names=col_compagnie, usecols=[1,2,3,4,6])
#print(compagnie)
compagnie.to_csv(r'C:\Users\cordi\Documents\projet_BDR\compagnie.csv',sep=';',index=False)




    
    
    
    
    
    
    
    
    
    