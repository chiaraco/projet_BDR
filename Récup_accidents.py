# -*- coding: utf-8 -*-

import pandas as pd
import csv
import numpy as np
import re

### Concatenation de tout les fichiers dans un dataframe
def creation_df():
    nom=['date','Victimes','localisation','Heure','Nom_Pays','Phase_de_vol','Nature_avion','Aeroport_depart','Aeroport_arrivee','Statut','Compagnie','Type_avion','Degats']
    fichier=['accident_1930_1939.csv','accident_1940_1949.csv','accident_1950_1959.csv','accident_1960_1969.csv','accident_1970_1979.csv','accident_1980_1989.csv','accident_1990_1999.csv','accident_2000_2009.csv','accident_2010_2020.csv']
    df=pd.read_csv('accident_1919_1929.csv',delimiter=';',usecols=[5,6,7,8,9,10,11,12,13,14,15,16,17],names=nom,encoding='utf8')#,errors='ignore')
    df.drop([0], inplace =True)
    for i in fichier:
        print(i)
        df1=pd.read_csv(i,delimiter=';',usecols=[5,6,7,8,9,10,11,12,13,14,15,16,17],names=nom,encoding='utf8')#,errors='ignore')
        df1.drop([0], inplace =True)
        df=pd.concat([df, df1])
    df.reset_index(drop=True,inplace=True)   
    
###Visualisation des colonnes
#    for i in nom:
#        print(i)
#        print(df[i].head(10))
#    print('taille',df.shape[0])
#    print(df.head())

    return(df)

###Ecriture d'un fichier .csv
def ecriture(df):
    with open('eggs.csv', 'w',encoding='utf-8',newline='') as csvfile:#newline evite d'avoir un saut de ligne entre chaque ligne
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(df)
        for i in range(0,df.shape[0]):
            spamwriter.writerow(df.loc[i])

###Ouverture nouveau fichier et test
def Nettoyage():
    df=pd.read_csv('Donnees_accidents.csv',delimiter=';', header=0)
    print(df.head())
    nom=['localisation','Heure','Phase_de_vol','Nature_avion','Aeroport_depart','Aeroport_arrivee','Statut','Compagnie','Type_avion','Degats','Fatalities','Occupants','Pays_accident','Pays_aeroport_depart','Pays_aeroport_arrivee','quatre_aeroport_depart','quatre_aeroport_arrivee','trois_aeroport_depart','trois_aeroport_arrivee','Minutes','jour','mois','annee']
    for i in nom:
        print(i)
        print(df[i].head(10))
        print()
    
    ####TESTE SUR LES REGEXS
    test=str('00:33 UTC')
    motif=re.compile(r"([0-9]{1,2}):([0-9]{2})")
    found=motif.search(test)
    if found:
        
        print(found.group(1))
        print(found.group(2))
        #print(found.group(3))
    else:
        print('Non trouvé')
    #print(df['date'])

    return df

### Nettoyage des dates
def jour(df):
    df['jour']=np.nan
    df['mois']=np.nan
    df['annee']=np.nan
    motif=re.compile(r"([0-9xX]*)\s([a-zA-Z]*)\s([0-9]{4})$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['date']
        found=motif.search(str(ligne))
        if found:
            jour=found.group(1)
            mois=found.group(2)
            annee=found.group(3)
            if ('x' or 'X') not in str(jour):
                df.loc[df.index[i],'jour']=str(jour)
            if ('x' or 'X') not in str(mois):
                df.loc[df.index[i],'mois']=str(mois)
            if ('x' or 'X') not in str(annee):
                df.loc[df.index[i],'annee']=str(annee)
        else:
            print(ligne)

    print(df['jour'])
    print(df['mois'])
    print(df['annee'])

    return(df)

###Nettoyage des heures
def time(df):
    #df['Minutes']=np.nan
    motif=re.compile(r"([0-9]{1,2}):([0-9]{2})")#([0-9]{1,2}):([0-9]{2})$")
    #motif2=re.compile(r"([0-9]{2}):([0-9]{2}) UTC$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Heure']
        found=motif.search(str(ligne))
        #found2=motif2.search(str(ligne))
        if found:
            heure=found.group(1)
            minutes=found.group(2)
            df.loc[df.index[i],'Minutes']=str(minutes)
            df.loc[df.index[i],'Heure']=str(heure)
#        elif found2:
#            heure=found2.group(1)
#            minutes=found2.group(2)
#            df.loc[df.index[i],'Minutes']=str(minutes)
#            df.loc[df.index[i],'Heure']=str(heure)
    print(df['Heure'])
    print(df['Minutes'])

    return(df)

###Nettoyage des aéroports
def nettoyageaero(df):
    motif=re.compile(r"(\(-\/-\))$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_depart']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            n=len(pays)+1
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)
    
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_arrivee']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            n=len(pays)+1
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)
    
    print(df['Aeroport_depart'])
    print(df['Aeroport_arrivee'])
    return(df)

## On enleve les aéroport inconnu (manque des aeroports, voir changement_aeroport)
def aeroport_dep_arr(df):
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_depart']
        ligne2=df.iloc[i]['Aeroport_arrivee']
        if ligne=='Unknown' or ligne=='-' or ligne=='?':
            df.loc[df.index[i],'Aeroport_depart']=np.nan   
        else:
            print('Non trouvé',str(ligne))
            #print('test',df.iloc[i]['Aeroport_depart'])
        if ligne2=='Unknown' or ligne2=='-' or ligne2=='?':
            df.loc[df.index[i],'Aeroport_arrivee']=np.nan   
        else:
            print('Non trouvé',str(ligne2))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
    print(df['Aeroport_depart'])
    print(df['Aeroport_arrivee'])

    return(df)

### On creé plusieurs colonne (pays_aero_dep,quatre_dep,trois_dep)
### Récupération de OACI et IATA
def aeroport_dep_arr2(df):
    df['quatre_aeroport_depart']=np.nan
    df['quatre_aeroport_arrivee']=np.nan
    
    ## DE LA FORME (XXX/XXXX)
    motif=re.compile(r"\/([A-Z]{4})\)$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_depart']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            df.loc[df.index[i],'quatre_aeroport_depart']=str(pays)
            n=len(pays)+1
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)  
        else:
            print('Non trouvé',str(ligne))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
        ligne2=df.iloc[i]['Aeroport_arrivee'] 
        found2=motif.search(str(ligne2))
        if found2:
            pays=found2.group(1)
            df.loc[df.index[i],'quatre_aeroport_arrivee']=str(pays)
            n=len(pays)+1
            m=len(ligne2)
            newloc=ligne2[0:(m-n)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)  
        else:
            print('Non trouvé',str(ligne2))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
    ## DE LA FORME (XXXX)
    motif=re.compile(r"\(([A-Z]{4})\)$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_depart']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            df.loc[df.index[i],'quatre_aeroport_depart']=str(pays)
            n=len(pays)+3
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)  
        else:
            print('Non trouvé',str(ligne))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
        ligne2=df.iloc[i]['Aeroport_arrivee'] 
        found2=motif.search(str(ligne2))
        if found2:
            pays=found2.group(1)
            df.loc[df.index[i],'quatre_aeroport_arrivee']=str(pays)
            n=len(pays)+3
            m=len(ligne2)
            newloc=ligne2[0:(m-n)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)  
        else:
            print('Non trouvé',str(ligne2))
            #print('test',df.iloc[i]['Aeroport_depart'])
    
    print(df['quatre_aeroport_depart'])
    print(df['Aeroport_depart'])
    print(df['quatre_aeroport_arrivee'])
    print(df['Aeroport_arrivee'])

    return(df)
    
    
### Suite du programme précédant    
def aeroport_dep_arr3(df):
    df['trois_aeroport_depart']=np.nan
    df['trois_aeroport_arrivee']=np.nan
    
    ## DE LA FORME (XXX/
    motif=re.compile(r"\(([A-Z]{3})\/$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_depart']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            df.loc[df.index[i],'trois_aeroport_depart']=str(pays)
            n=len(pays)+3
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)  
        else:
            print('Non trouvé',str(ligne))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
        ligne2=df.iloc[i]['Aeroport_arrivee'] 
        found2=motif.search(str(ligne2))
        if found2:
            pays=found2.group(1)
            df.loc[df.index[i],'trois_aeroport_arrivee']=str(pays)
            n=len(pays)+3
            m=len(ligne2)
            newloc=ligne2[0:(m-n)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)  
        else:
            print('Non trouvé',str(ligne2))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
    ## DE LA FORME (XXX)
    motif=re.compile(r"\(([A-Z]{3})\)$")
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Aeroport_depart']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            df.loc[df.index[i],'trois_aeroport_depart']=str(pays)
            n=len(pays)+3
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)  
        else:
            print('Non trouvé',str(ligne))
            #print('test',df.iloc[i]['Aeroport_depart'])
            
        ligne2=df.iloc[i]['Aeroport_arrivee'] 
        found2=motif.search(str(ligne2))
        if found2:
            pays=found2.group(1)
            df.loc[df.index[i],'trois_aeroport_arrivee']=str(pays)
            n=len(pays)+3
            m=len(ligne2)
            newloc=ligne2[0:(m-n)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)  
        else:
            print('Non trouvé',str(ligne2))
            #print('test',df.iloc[i]['Aeroport_depart'])
    
    print(df['trois_aeroport_depart'])
    print(df['Aeroport_depart'])
    print(df['trois_aeroport_arrivee'])
    print(df['Aeroport_arrivee'])

    return(df)

    
### On nettoie la colonne nature_avion
def Nature_avion(df):
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Nature_avion']
        if ligne=='Unknown' or ligne=='-':
            df.loc[df.index[i],'Nature_avion']=np.nan
            
        else:
            print('Non trouvé',str(ligne))
            print('test',df.iloc[i]['Nature_avion'])
            
    print(df['Nature_avion'])
    return(df)

### On modifie Phase de vol
def phase_de_vol(df):
    motif=re.compile(r'\(([a-zA-Z]{3})\)$')
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Phase_de_vol']
        found=motif.search(str(ligne))
        if found:
            a=found.group(1)
            n=len(a)+2
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'Phase_de_vol']=str(newloc)
            
        else:
            print('Non trouvé',str(ligne))
            print('test',df.iloc[i]['Phase_de_vol'])
            
    print(df['Phase_de_vol'])
    return(df)
    
    
###On rajoute la colonne Pays_accident et on modifie localisation 
def localisation(df):
    df['Pays_accident']=np.nan
    motif=re.compile(r"\(([a-zA-Z\sãéí.'ç-]*)\)$")#.'-çãé
    for i in range(0,len(df)):
        ligne=df.iloc[i]['localisation']
        found=motif.search(str(ligne))
        if found:
            pays=found.group(1)
            df.loc[df.index[i],'Pays_accident']=str(pays)
            n=len(pays)+2
            m=len(ligne)
            newloc=ligne[0:(m-n)]
            df.loc[df.index[i],'localisation']=str(newloc)
            
        else:
            print('Non trouvé',str(ligne))
            print('pays',df.iloc[i]['Nom_Pays'])
            
    print(df['Pays_accident'])
    print(df['localisation'])
    return(df)
    
###On sépare fatalities et occupants
def Victime(df): 
    df['Fatalities']=np.nan
    df['Occupants']=np.nan
    motif=re.compile(r'Fatalities: ([0-9]+) \/ Occupants: ([0-9]+)$')
    for i in range(0,len(df)):
        ligne=df.iloc[i]['Victimes']
        found=motif.search(str(ligne))
        if found:# il y a t il des cas ou 1 nan et l'autre un nbr ???
            df.loc[df.index[i],'Fatalities']=int(found.group(1))
            df.loc[df.index[i],'Occupants']=int(found.group(2))
    print(df['Fatalities'])
    print(df['Occupants'])
    return df

###On change les mois en numéro
def mois(df):
    for i in range(len(df)):
        mois=df.iloc[i]['mois']
        if mois=='January' or mois=='JAN':
            df.loc[df.index[i],'mois']=1
        elif mois=='February' or mois=='FEB':
            df.loc[df.index[i],'mois']=2
        elif mois=='March' or mois=='MAR':
            df.loc[df.index[i],'mois']=3
        elif mois=='April' or mois=='APR':
            df.loc[df.index[i],'mois']=4
        elif mois=='May' or mois=='MAY':
            df.loc[df.index[i],'mois']=5
        elif mois=='June' or mois=='JUN':
            df.loc[df.index[i],'mois']=6
        elif mois=='July' or mois=='JUL':
            df.loc[df.index[i],'mois']=7
        elif mois=='August' or mois=='AUG':
            df.loc[df.index[i],'mois']=8
        elif mois=='September' or mois=='SEP':
            df.loc[df.index[i],'mois']=9
        elif mois=='October' or mois=='OCT':
            df.loc[df.index[i],'mois']=10
        elif mois=='November' or mois=='NOV':
            df.loc[df.index[i],'mois']=11
        elif mois=='December' or mois=='DEC':
            df.loc[df.index[i],'mois']=12
        elif mois=='XXX':
            df.loc[df.index[i],'mois']=np.nan
        else:
            print(mois)
    print(df['mois'])
    return(df)
        
        
#df=Nettoyage()
#DF=mois(df)
#DF=jour(df)
#DF=time(df)
#DF=nettoyageaero(df)

#DF=aeroport_dep_arr3(df)
#DF=Nature_avion(df)
#DF=localisation(df)
#DF=Victime(df)
#df=ouverture()
#ecriture(df)    
    
    
###################  DEUXIEME PARTIE DU NETTOYAGE ##########################

def Ouverture():
    df=pd.read_csv('Donnees_accidents8.csv',delimiter=';', header=0)
    print(df.head())
    nom=['localisation','Heure','Phase_de_vol','Nature_avion','Aeroport_depart','Aeroport_arrivee','Statut','Compagnie','Type_avion','Degats','Fatalities','Occupants','Pays_accident','Pays_aeroport_depart','Pays_aeroport_arrivee','quatre_aeroport_depart','quatre_aeroport_arrivee','trois_aeroport_depart','trois_aeroport_arrivee','Minutes','jour','mois','annee']
    for i in nom:
        print(i)
        print(df[i].head(10))
        print()


    ####TESTE SUR LES REGEXS
    test=str('McDonnell Douglas DC-10-110')#Douglas DC-6BF')#Douglas C-54G Skymaster (DC-4)')#Douglas C-118A Liftmaster (DC-6A)')
    motif=re.compile(r"^McDonnell Douglas DC-([0-9]*)-\w*$")
    found=motif.search(test)
    if found:
        a='Antonov An-'+found.group(1)
        print(a)

    else:
        print('Non trouvé')
    
    #print(df['Type_avion'])
    return df

def changement_pays(df):
    motif=re.compile(r"(United States of America)")
    motif2=re.compile(r"(Unknown country)")
    motif3=re.compile(r"(unknown country)")
    for i in range(len(df)):
        ligne=df.iloc[i]['Pays_accident']
        found=motif.search(str(ligne))
        found2=motif2.search(str(ligne))
        found3=motif3.search(str(ligne))
        if found:
            df.loc[df.index[i],'Pays_accident']='United States'
        if found2 or found3:
            df.loc[df.index[i],'Pays_accident']=np.nan
        if str(ligne)=='Atlantic Ocean' or str(ligne)=='Arctic Ocean' or str(ligne)=='Pacific Ocean' or str(ligne)=='Mediterranean Sea' or str(ligne)=='Indian Ocean':
            df.loc[df.index[i],'Pays_accident']=np.nan
        if str(ligne)=='Democratic Republic of the Congo':
            df.loc[df.index[i],'Pays_accident']='DR Congo'
        if str(ligne)=='Saint Lucia':
            df.loc[df.index[i],'Pays_accident']='St. Lucia'
        if str(ligne)=='U.S. Virgin Islands':
            df.loc[df.index[i],'Pays_accident']='United States Virgin Islands'
        if str(ligne)=='U.S. Minor Outlying Islands':
            df.loc[df.index[i],'Pays_accident']='United States'
        if str(ligne)=='Kyrgyzstan':
            df.loc[df.index[i],'Pays_accident']='Kyrgyz Republic'
        if str(ligne)=='Curaçao':
            df.loc[df.index[i],'Pays_accident']='Netherlands Antilles'
        if str(ligne)=='Saint Vincent and the Grenadines':
            df.loc[df.index[i],'Pays_accident']='St. Vincent and the Grenadines'
        if str(ligne)=='Micronesia':
            df.loc[df.index[i],'Pays_accident']='Micronesia, Fed. Sts.'
        if str(ligne)=='North Macedonia':
            df.loc[df.index[i],'Pays_accident']='Macedonia'
        if str(ligne)=='Cape Verde':
            df.loc[df.index[i],'Pays_accident']='Cabo Verde'
        if str(ligne)=='São Tomé and Príncipe':
            df.loc[df.index[i],'Pays_accident']='Sao Tome and Principe'
        if str(ligne)=='Sint Maarten':
            df.loc[df.index[i],'Pays_accident']='Netherlands Antilles'
        if str(ligne)=='Congo':
            df.loc[df.index[i],'Pays_accident']='Congo Republic'
        #if str(ligne)=='Kosovo':
            #df.loc[df.index[i],'Pays_accident']=''
        if str(ligne)=='East Timor':
            df.loc[df.index[i],'Pays_accident']='Timor-Leste'
        if str(ligne)=='Caribbean Netherlands':
            df.loc[df.index[i],'Pays_accident']='Netherlands Antilles'
        if str(ligne)=='Macau':
            df.loc[df.index[i],'Pays_accident']='Macao'
    print(df['Pays_accident'])
    return df

def changement_aeroport(df):
    motif=re.compile(r"(unknown)")
    for i in range(len(df)):
        ligne_dep=df.iloc[i]['Aeroport_depart']
        ligne_arr=df.iloc[i]['Aeroport_arrivee']
        found=motif.search(str(ligne_dep))
        found_arr=motif.search(str(ligne_arr))
        if found:
            df.loc[df.index[i],'Aeroport_depart']=np.nan
            #print(str(df.iloc[i]['Aeroport_depart']))
        if found_arr:
            df.loc[df.index[i],'Aeroport_arrivee']=np.nan
            #print(str(df.iloc[i]['Aeroport_arrivee']))
    
    motif2=re.compile(r"(, [A-Z]{2})$")
    motif3=re.compile(r"(, [A-Z]{3})$")
    for i in range(len(df)):
        ligne_dep=df.iloc[i]['Aeroport_depart']
        ligne_arr=df.iloc[i]['Aeroport_arrivee']
        found2=motif2.search(str(ligne_dep))
        found2_arr=motif2.search(str(ligne_arr))
        if found2:
            a=len(ligne_dep)
            newloc=ligne_dep[0:(a-4)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)
        if found2_arr:
            a=len(ligne_arr)
            newloc=ligne_arr[0:(a-4)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)
            
        found3=motif3.search(str(ligne_dep))
        found3_arr=motif3.search(str(ligne_arr))
        if found3:
            a=len(ligne_dep)
            newloc=ligne_dep[0:(a-5)]
            df.loc[df.index[i],'Aeroport_depart']=str(newloc)
        if found3_arr:
            a=len(ligne_arr)
            newloc=ligne_arr[0:(a-5)]
            df.loc[df.index[i],'Aeroport_arrivee']=str(newloc)
        
    print(df['Aeroport_depart'])
    print(df['Aeroport_arrivee'])
    return(df)
    
def changement_modele(df):
    #print(df['Type_avion'])
    motif=re.compile(r"^(Boeing [0-9]{3}-[0-9]{1})\w*$")
    #motif=re.compile(r"^Cessna [\w-]* (Citation [I]*)$")
    motif2=re.compile(r"^British Aerospace [\w-]* (Jetstream [0-9]{2})")
    motif3=re.compile(r"^Douglas [\w\s-]*\((DC-[\w]*)\)$")
    for i in range(len(df)):
        ligne=df.iloc[i]['Type_avion']
        found=motif.search(str(ligne))
        if found:
            a=found.group(1)+'00'
            df.loc[df.index[i],'Type_avion']=a
            #print(str(df.iloc[i]['Aeroport_depart']))
        
        found2=motif2.search(str(ligne))
        if found2:
            a='British Aerospace '+found2.group(1)
            df.loc[df.index[i],'Type_avion']=a
        
        found3=motif3.search(str(ligne))
        if found3:
            a='Douglas '+found3.group(1)
            df.loc[df.index[i],'Type_avion']=a
    
    motif=re.compile(r"^Douglas (DC-[0-9]*)[A-Za-z]*$")
    for i in range(len(df)):
        ligne=df.iloc[i]['Type_avion']
        found=motif.search(str(ligne))
        if found:
            a='Douglas '+found.group(1)
            df.loc[df.index[i],'Type_avion']=a
    return df

def changement_modele2(df):
    motif=re.compile(r"^Fokker F-([0-9]{2} \w*ship)")
    motif2=re.compile(r"^Antonov An-([0-9]*)\w*")
    motif3=re.compile(r"^Ilyushin [a-zA-Z-]*([0-9]+)\w*")
    motif4=re.compile(r"^Cessna [\w-]* Citation \w*?/*([I]{1,3})")
    motif5=re.compile(r"^Lockheed [\w-]* (Hercules)")
    motif6=re.compile(r"^Lockheed [\w-]* (TriStar)")
    motif7=re.compile(r"^Lockheed [\w-]* (Super Constellation)")
    motif8=re.compile(r"^Lockheed [\w-]* (Electra)")
    motif9=re.compile(r"^Tupolev Tu-([0-9]*)\w*")
    motif10=re.compile(r"^McDonnell Douglas DC-([0-9]*)-\w*$")
    for i in range(len(df)):
        ligne=df.iloc[i]['Type_avion']
        found=motif.search(str(ligne))
        found2=motif2.search(str(ligne))
        found3=motif3.search(str(ligne))
        found4=motif4.search(str(ligne))
        found5=motif5.search(str(ligne))
        found6=motif6.search(str(ligne))
        found7=motif7.search(str(ligne))
        found8=motif8.search(str(ligne))
        found9=motif9.search(str(ligne))
        found10=motif10.search(str(ligne))
        if found:
            a='Fokker F'+found.group(1)
            df.loc[df.index[i],'Type_avion']=a
        if found2:
            a='Antonov An-'+found2.group(1)
            df.loc[df.index[i],'Type_avion']=a
        if found3:
            a='Ilyushin IL'+found3.group(1)
            df.loc[df.index[i],'Type_avion']=a
        if found4:
            a='Cessna Citation '+found4.group(1)
            df.loc[df.index[i],'Type_avion']=a  
        if found5:
            a='Lockheed L-182 / 282 / 382 (L-100) Hercules'
            df.loc[df.index[i],'Type_avion']=a
        if found6:
            a='Lockheed L-1011 Tristar'
            df.loc[df.index[i],'Type_avion']=a
        if found7:
            a='Lockheed L-1049 Super Constellation'
            df.loc[df.index[i],'Type_avion']=a
        if found8:
            a='Lockheed L-188 Electra'
            df.loc[df.index[i],'Type_avion']=a
        if found9:
            a='Tupolev Tu-'+found9.group(1)
            df.loc[df.index[i],'Type_avion']=a
        if found10:
            a='McDonnell Douglas DC-'+a
            df.loc[df.index[i],'Type_avion']=a
    return(df)
df=Ouverture()
df2=changement_pays(df)
#df3=changement_aeroport(df2)
#df4=changement_modele2(df2)
ecriture(df2)