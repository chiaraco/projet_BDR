#!/usr/bin/env python3
#-*- coding: utf-8 -*-

""" Peuplement des tables """

import pandas as pd
from monappli.models import Pays, Avion, Aeroport, Compagnie


pays=pd.read_csv('pays.csv',sep=';')
avion=pd.read_csv('avion.csv',sep=';')
aeroport=pd.read_csv('aeroport.csv',sep=';')
compagnie=pd.read_csv('compagnie.csv',sep=';')



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
    
