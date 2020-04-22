#!/usr/bin/env python3
#-*- coding: utf-8 -*-



""" Récupération des données du site https://openflights.org/data.html """

# on récupère seulement les colonnes qui nous intéressent
# et on les mémorise dans des dataframe


import pandas as pd
import re
import numpy as np

col_pays=["Pays","ISO"]
pays=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat", delimiter=",", names=col_pays, usecols=[0,1])
#print(pays)
motif =re.compile(r"\\N")
len_ISO=[]
len_Nom=[]
pays.loc[pays.index[251],'ISO']=''
for i in range(len(pays)):
    ligne=pays.iloc[i]['ISO']
    ligne2=pays.iloc[i]['Pays']

    found=motif.search(str(ligne))
    if found :
        pays.loc[pays.index[i],'ISO']=''
    
    if len(str(ligne))==3:
        print(ligne)
        print(str(ligne))
        print(i,type(ligne))
    len_Nom.append(len(str(ligne2)))
    len_ISO.append(len(str(ligne)))
print(max(len_ISO),max(len_Nom))
pays.to_csv(r'pays.csv',sep=';',index=False)


col_avion=["Modele","IATA","OACI"]
avion=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/planes.dat", delimiter=",", names=col_avion, usecols=[0,1,2])
#print(avion)
avion.to_csv(r'C:\Users\cordi\Documents\projet_BDR\avion.csv',sep=';',index=False)


col_aeroport=["Nom","Ville","Pays","IATA","OACI","Lat","Lon","Alt"]
aeroport=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat", delimiter=",", names=col_aeroport, usecols=[1,2,3,4,5,6,7,8])
#print(aeroport)

ville=aeroport.loc[:,["Ville","Pays"]]
ville.to_csv(r'C:\Users\cordi\Documents\projet_BDR\ville.csv',sep=';',index=False)

del(aeroport["Pays"])
aeroport.to_csv(r'C:\Users\cordi\Documents\projet_BDR\aeroport.csv',sep=';',index=False)


col_compagnie=["Nom","Alias","IATA","OACI","Pays"]
compagnie=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat", delimiter=",", names=col_compagnie, usecols=[1,2,3,4,6])
#print(compagnie)
len_IATA=[]
len_OACI=[]
for i in range(len(compagnie)):
    ligne=compagnie.iloc[i]['IATA']
    ligne2=compagnie.iloc[i]['OACI']
    if str(ligne)=='nan':
        compagnie.loc[compagnie.index[i],'IATA']=''
        print(i,ligne,type(ligne),"IATA")
    if len(str(ligne2))>3:   
        print(i,ligne2,type(ligne2),"OACI")
    len_IATA.append(len(str(ligne)))
    len_OACI.append(len(str(ligne2)))
print(max(len_IATA),max(len_OACI))
compagnie.to_csv(r'compagnie.csv',sep=';',index=False)


    
    
    
    
    
    
    