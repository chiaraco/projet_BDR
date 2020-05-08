#!/usr/bin/env python3
#-*- coding: utf-8 -*-



""" Récupération des données du site https://openflights.org/data.html """

# on récupère seulement les colonnes qui nous intéressent
# et on les mémorise dans des dataframe


import pandas as pd
import re
import numpy as np

motif_vide = re.compile(r"\\N")
# ISO, IATA et OACI prenne une de ces formes :
motif2 = re.compile(r"[a-zA-Z0-9]{2}")
motif3 = re.compile(r"[a-zA-Z0-9]{3}")
motif4 = re.compile(r"[a-zA-Z0-9]{4}")



###### PAYS ######

col_pays=["Pays","ISO"]
pays=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/countries.dat", delimiter=",", names=col_pays, usecols=[0,1], dtype="str")

for i in range(len(pays)):

    # on règle le problème des NaN
    if not isinstance(pays.iloc[i][1], str) :
        pays.iloc[i][1]=""
    
    # on règle le problème des \N (équivalents à NaN)
    # tout en vérifiant que ISO est de la bonne forme
    found2=motif2.search(pays.iloc[i][1])
    if found2 :
        pays.iloc[i][1]=found2.group()
    else : 
        pays.iloc[i][1]=""

#print(pays)
pays.to_csv(r'C:\Users\cordi\Documents\Aide Projet BDR\mes_donnees\pays.csv',sep=';',index=False)



###### AVION ######

col_avion=["Modele","IATA","OACI"]
avion=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/planes.dat", delimiter=",", names=col_avion, usecols=[0,1,2], dtype="str")

for j in range(1,3):
    
    for i in range(len(avion)):
    
        # on règle le problème des NaN
        if not isinstance(avion.iloc[i][j], str) :
            avion.iloc[i][j]=""
            print(avion.iloc[i][j])
            print(type(avion.iloc[i][j]))
        # on règle le problème des \N (équivalents à NaN)
        found=motif_vide.search(avion.iloc[i][j])
        if found :
            avion.iloc[i][j]=""
            
        # on vérifie que IATA et OACI sont de la bonne forme
        if j==1:
            found3=motif3.search(avion.iloc[i][j])
            if found3 : avion.iloc[i][j]=found3.group()
            else : avion.iloc[i][j]=""
        if j==2:
            found4=motif4.search(avion.iloc[i][j])
            if found4 : avion.iloc[i][j]=found4.group()
            else : avion.iloc[i][j]=""
            
#print(avion)
avion.to_csv(r'C:\Users\cordi\Documents\Aide Projet BDR\mes_donnees\avion.csv',sep=';',index=False)



###### AEROPORT ET VILLE ######

col_aeroport=["Nom","Ville","Pays","IATA","OACI","Lat","Lon","Alt"]
aeroport=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat", delimiter=",", names=col_aeroport, usecols=[1,2,3,4,5,6,7,8], dtype={"Nom":"str","Ville":"str","Pays":"str","IATA":"str","OACI":"str","Lat":np.float64,"Lon":np.float64,"Alt":np.int64})

## Problème des aéroports ayant le même nom
occ_ae={} # dictionnaire, à un aeroport on associe son occurrence
for i in range(len(aeroport)):
    if aeroport.iloc[i,0] not in occ_ae.keys() :
        occ_ae[aeroport.iloc[i,0]]=1
    else :
        occ_ae[aeroport.iloc[i,0]]+=1
        aeroport.iloc[i,0] = str(aeroport.iloc[i,0]) + " " + str(occ_ae[aeroport.iloc[i,0]])
        

for j in range(1,7):
    
    for i in range(len(aeroport)):
    
        # on règle le problème des NaN
        if (j in [1,2,3,4]) and not isinstance(aeroport.iloc[i,j], str) :
            aeroport.iloc[i,j]=""
        
        # on règle le problème des \N (équivalents à NaN)
        found=motif_vide.search(str(aeroport.iloc[i,j]))
        if found :
            aeroport.iloc[i,j]=""
            
        # on vérifie que IATA et OACI sont de la bonne forme
        if j==3:
            found3=motif3.search(aeroport.iloc[i,j])
            if found3 : aeroport.iloc[i,j]=found3.group()
            else : aeroport.iloc[i,j]=""
        if j==4:
            found4=motif4.search(aeroport.iloc[i,j])
            if found4 : aeroport.iloc[i,j]=found4.group()
            else : aeroport.iloc[i,j]=""

#print(aeroport)
aeroport.to_csv(r'C:\Users\cordi\Documents\Aide Projet BDR\mes_donnees\aeroportV1.csv',sep=';',index=False)



###### COMPAGNIE ######

col_compagnie=["Nom","Alias","IATA","OACI","Pays"]
compagnie=pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat", delimiter=",", names=col_compagnie, usecols=[1,2,3,4,6], dtype="str")

compagnie.drop(0, inplace=True)
compagnie.reset_index(inplace=True,drop=True)

max_alias=-1

for j in range(1,5):
    
    for i in range(len(compagnie)):
    
        # on règle le problème des NaN
        if not isinstance(compagnie.iloc[i][j], str) :
            compagnie.iloc[i][j]=""

        # on règle le problème des \N (équivalents à NaN)
        found=motif_vide.search(compagnie.iloc[i][j])
        if found :
            compagnie.iloc[i][j]=""
            
        # on vérifie que IATA et OACI sont de la bonne forme
        if j==2:
            found2=motif2.search(compagnie.iloc[i][j])
            if found2 : compagnie.iloc[i][j]=found2.group()
            else : compagnie.iloc[i][j]=""
        if j==3:
            found3=motif3.search(compagnie.iloc[i][j])
            if found3 : compagnie.iloc[i][j]=found3.group()
            else : compagnie.iloc[i][j]=""
        
        # on récupère la longueur max des alias
        if j==1: 
            l=len(compagnie.iloc[i][j])
            if l > max_alias : max_alias = l
        
print(max_alias) #30
#print(compagnie)
compagnie.to_csv(r'C:\Users\cordi\Documents\Aide Projet BDR\mes_donnees\compagnieV1.csv',sep=';',index=False)


    
    
    
    
    
    
    
