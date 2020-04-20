#!/usr/bin/env python3
#-*- coding: utf-8 -*-

""" Peuplement des tables """

import pandas as pd
from monappli.models import Pays, Avion, Aeroport, Compagnie, Ville


pays=pd.read_csv('pays.csv',sep=';')
avion=pd.read_csv('avion.csv',sep=';')
aeroport=pd.read_csv('aeroport.csv',sep=';')
compagnie=pd.read_csv('compagnie.csv',sep=';')
ville=pd.read_csv('ville.csv',sep=';')



for i in range(len(pays)) : 
    pa = Pays(NomPays=pays.iloc[i][0], ISO=pays.iloc[i][1])
    pa.save


for j in range(len(ville)) :
    vi = Ville(NomVille=ville.iloc[j][0], NomPays=ville.iloc[j][1])
    vi.save
  
    
for k in range(len(avion)) : 
    av = Avion(Modele=avion.iloc[k][0], IATA=avion.iloc[k][1], OACI=avion.iloc[k][2])
    av.save
    

for l in range(len(aeroport)) : 
    ae = Aeroport(NomAeroport=aeroport.iloc[l][0], IATA=aeroport.iloc[l][3], OACI=aeroport.iloc[l][4], Latitude=aeroport.iloc[l][5], Longitude=aeroport.iloc[l][6], Altitude=aeroport.iloc[l][7], Ville=aeroport.iloc[l][1], NomPays=aeroport.iloc[l][2])
    ae.save   
    
    
for m in range(len(compagnie)) : 
    co = Compagnie(NomCompagnie=compagnie.iloc[m][0], Alias=compagnie.iloc[m][1], IATA=compagnie.iloc[m][2], OACI=compagnie.iloc[m][3], NomPays=compagnie.iloc[m][4])
    co.save  
    
