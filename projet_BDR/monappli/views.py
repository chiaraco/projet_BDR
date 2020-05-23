from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville
import datetime
from django.db.models import Count
import matplotlib.pyplot as plt
import numpy as np
import os



"""Page d'accueil"""
def accueil(request):
	return render(request,'accueil.tmpl')



"""Page récapitulative des tables de données"""
def donnees(request):
	return render(request,'choix_table.tmpl')

	
	
"""Page des pays"""	
def pays(request):

	## Si aucune recherche effectuée
	if not request.GET.keys():
		return render(request, 'pays.tmpl', 
			{                                          
        	    'pays': Pays.objects.all().order_by('nom_pays'),
        	    'nb': Pays.objects.count()-1,
			    'rien': Pays.objects.count()==0
			})
			
	## Sinon 
	else :
		pays_iso=request.GET['pays_iso'] #récupère la recherche
		pa_iso=Pays.objects.none()
		
		if 'chercher_iso' in request.GET.keys(): #si la checkbox de ISO est cochée
			iso=Pays.objects.filter(iso__icontains=pays_iso)
			pa_iso=iso
			
		if 'chercher_pays' in request.GET.keys(): #si la checkbox de pays est cochée
			pa=Pays.objects.filter(nom_pays__icontains=pays_iso)
			
			pa_iso=pa_iso | pa #union des 2 requêtes
			
		return render(request, 'pays.tmpl', 
			{                                          
        	   	'pays': pa_iso.order_by('nom_pays'),
        	   	'nb': pa_iso.count(),
	    	    'rien': pa_iso.count()==0
	    	})

	
	
"""Page des villes"""	
def ville(request):

	## Si aucune recherche effectuée
	if not request.GET.keys(): 
		return render(request, 'ville.tmpl', 
		{                                          
           	'ville': Ville.objects.all().order_by('nom_ville'),
           	'nb': Ville.objects.count()-1,
	        'rien': Ville.objects.count()==0
	    })
	
	## Sinon 
	else :
		vi_pa=Ville.objects.none()
		pays_ville=request.GET['pays_ville'] #récupère la recherche
		
		if 'chercher_ville' in request.GET.keys(): #si la checkbox de ville est cochée
			vi=Ville.objects.filter(nom_ville__icontains=pays_ville)
			vi_pa=vi
			
		if 'chercher_pays' in request.GET.keys(): #si la checkbox de pays est cochée
			pays=Pays.objects.filter(nom_pays__icontains=pays_ville)
			pa=Ville.objects.filter(nom_pays__in=pays)
			
			vi_pa=vi_pa | pa #union des 2 requêtes

		return render(request, 'ville.tmpl', 
		{                                          
           	'ville': vi_pa.order_by('nom_ville'),
           	'nb': vi_pa.count(),
	        'rien': vi_pa.count()==0
	    })

	
	
"""Page des avions"""			
def avion(request):

	## Si aucune recherche effectuée
	if not request.GET.keys():
		return render(request, 'avion.tmpl', 
	    	{                                          
	        	'avion': Avion.objects.all().order_by('modele'),
	        	'nb': Avion.objects.count()-1,
	        	'rien': Avion.objects.count()==0
	    	})
	
	## Sinon
	else :
		av=Avion.objects.none()
		rech_avion=request.GET['rech_avion'] #récupère la recherche
		
		if 'chercher_modele' in request.GET.keys(): #si la checkbox de modèle est cochée
			av=Avion.objects.filter(modele__icontains=rech_avion)
			
		if 'chercher_iata' in request.GET.keys(): #si la checkbox de IATA est cochée
			iata=Avion.objects.filter(iata__icontains=rech_avion)
			av=av | iata #union
			
		if 'chercher_oaci' in request.GET.keys(): #si la checkbox de OACI est cochée
			oaci=Avion.objects.filter(oaci__icontains=rech_avion)
			av=av | oaci #union

		return render(request, 'avion.tmpl', 
		{                                          
           	'avion': av.order_by('modele'),
           	'nb': av.count(),
	        'rien': av.count()==0
	    })

	
	
"""Page des compagnies"""		    
def compagnie(request):

	## Si aucune recherche effectuée
	if not request.GET.keys():
		return render(request, 'compagnie.tmpl', 
	    	{                                          
	        	'compagnie': Compagnie.objects.all().order_by('nom_compagnie'),
	        	'nb': Compagnie.objects.count()-1,
	        	'rien': Compagnie.objects.count()==0
	   		})
	
	## Sinon
	else :
		comp=Compagnie.objects.all()
		rech_compagnie=request.GET['rech_compagnie'] #récupère la recherche
		
		## union de la recherche sur nom et alias
		union=Compagnie.objects.none()
		
		if 'chercher_compagnie' in request.GET.keys(): #si la checkbox de compagnie est cochée
			union=Compagnie.objects.filter(nom_compagnie__icontains=rech_compagnie)
			
		if 'chercher_alias' in request.GET.keys(): #si la checkbox de alias est cochée
			union=union | Compagnie.objects.filter(alias__icontains=rech_compagnie)
			
		comp=comp & union

		## recherche d'un code
		code=request.GET['code']
		if ('co' in request.GET.keys()) and (code!=''):
			co=request.GET['co']
			#si la radio de IATA est cochée
			if co=='iata':
				iata=Compagnie.objects.filter(iata__iexact=code)
				comp=comp & iata
			#si la radio de OACI est cochée				
			elif co=='oaci':
				oaci=Compagnie.objects.filter(oaci__iexact=code)
				comp=comp & oaci
	
		## recherche du pays
		chercher_pays=request.GET['chercher_pays']
		if not chercher_pays=='':
			pays=Pays.objects.filter(nom_pays__icontains=chercher_pays)			
			pa=Compagnie.objects.filter(nom_pays__in=pays)
			comp=comp & pa
		
		return render(request, 'compagnie.tmpl', 
		{                                          
           	'compagnie': comp.order_by('nom_compagnie'),
           	'nb': comp.count(),
	        'rien': comp.count()==0
	    })

	
	
"""Page des aéroports"""	
def aeroport(request):

	## Si aucune recherche effectuée
	if not request.GET.keys():
		return render(request, 'aeroport.tmpl', 
		    {                                          
		        'aeroport': Aeroport.objects.all().order_by('nom_aeroport'),
		        'nb': Aeroport.objects.count()-1,
		        'rien': Aeroport.objects.count()==0,
		    })

	## Sinon		 
	else :
		liste=Aeroport.objects.all()
		
		aero=request.GET['aero'] # récupère la recherche du nom de l'aéroport
		if not aero=='':
			nom=Aeroport.objects.filter(nom_aeroport__icontains=aero)
			liste=liste & nom
		
		## recherche d'un code
		code=request.GET['code']
		if ('co' in request.GET.keys()) and (code!=''):
			co=request.GET['co']
			#si la radio de IATA est cochée	
			if co=='iata':
				iata=Aeroport.objects.filter(iata__iexact=code)
				liste=liste & iata	
			#si la radio de OACI est cochée				
			elif co=='oaci':
				oaci=Aeroport.objects.filter(oaci__iexact=code)
				liste=liste & oaci
		
		#si la checkbox de ville est cochée	
		if 'chercher_ville' in request.GET.keys():
			ville=Ville.objects.filter(nom_ville__icontains=vipa)
			ae=Aeroport.objects.filter(ville__in=ville)
			liste=liste & ae
		
		#si la checkbox de pays est cochée	
		if 'chercher_pays' in request.GET.keys():
			pays=Pays.objects.filter(nom_pays__icontains=vipa)
			ville=Ville.objects.filter(nom_pays__in=pays)
			ae=Aeroport.objects.filter(ville__in=ville)
			liste=liste & ae
			
		return render(request, 'aeroport.tmpl',
		{
			'aeroport': vi_pa.order_by('nom_aeroport'),
			'nb': vi_pa.count(),
			'rien': vi_pa.count()==0
		})

	
	
"""Page des accidents"""		    
def accident(request):
	
	##On initialise pour pas d'affichage de graphe
	bool_fig=False
	
	##On initialise à tous les accidents
	#puis on fera une intersection de toutes les requêtes
	liste=Accident.objects.all()
	
	## Si aucune recherche effectuée
	if not request.GET.keys():
		return render(request, 'accident.tmpl', 
	    	{                                          
	        	'accident': liste.order_by('time'),
	        	'nb': liste.count(),
	        	'rien': liste.count()==0,
				'bool_fig': bool_fig
	   	})

	## Sinon
	elif 'depart' in request.GET.keys():
	
		#recherche du départ (soit pays soit ville soit aéroport)
		depart=request.GET['depart']
		if not depart=='':
			aero=Aeroport.objects.filter(nom_aeroport__icontains=depart)
			dep=Accident.objects.filter(id_aeroport_depart__in=aero)

			pays=Pays.objects.filter(nom_pays__icontains=depart)
			pays_ville=Ville.objects.filter(nom_pays__in=pays)
			pays_aero=Aeroport.objects.filter(ville__in=pays_ville)
			dep= dep | Accident.objects.filter(id_aeroport_depart__in=pays_aero)

			ville=Ville.objects.filter(nom_ville__icontains=depart)
			ville_aero=Aeroport.objects.filter(ville__in=ville)
			dep= dep | Accident.objects.filter(id_aeroport_depart__in=ville_aero)
		
			liste=liste & dep
	
		#recherche de l'arrivée (soit pays soit ville soit aéroport)
		arrivee=request.GET['arrivee']
		if not arrivee=='':
			aero=Aeroport.objects.filter(nom_aeroport__icontains=arrivee)
			arr=Accident.objects.filter(id_aeroport_arrivee__in=aero)

			pays=Pays.objects.filter(nom_pays__icontains=arrivee)
			pays_ville=Ville.objects.filter(nom_pays__in=pays)
			pays_aero=Aeroport.objects.filter(ville__in=pays_ville)
			arr= arr | Accident.objects.filter(id_aeroport_arrivee__in=pays_aero)

			ville=Ville.objects.filter(nom_ville__icontains=arrivee)
			ville_aero=Aeroport.objects.filter(ville__in=ville)
			arr= arr | Accident.objects.filter(id_aeroport_arrivee__in=ville_aero)

			liste=liste & arr
		
		#recherche du lieu de l'accident (pays ou emplacement)
		lieu=request.GET['lieu']
		if not lieu=='':
			liste_lieu=Accident.objects.filter(emplacement__icontains=lieu)

			pays=Pays.objects.filter(nom_pays__icontains=lieu)
			pa=Accident.objects.filter(nom_pays__in=pays)
			liste_lieu=liste_lieu | pa

			liste=liste & liste_lieu
		
		#recherche de la compagnie
		compagnie=request.GET['compagnie']
		if not compagnie=='':
			comp=Compagnie.objects.filter(nom_compagnie__icontains=compagnie)
			comp=comp | Compagnie.objects.filter(alias__icontains=compagnie)
			comp=comp | Compagnie.objects.filter(iata__iexact=compagnie)
			comp=comp | Compagnie.objects.filter(oaci__iexact=compagnie)
			co=Accident.objects.filter(nom_compagnie__in=comp)
			liste= liste & co
		
		#recherche de l'avion
		avion=request.GET['avion']
		if not avion=='':
			av=Avion.objects.filter(modele__icontains=avion)
			av=av | Avion.objects.filter(iata__iexact=avion)
			av=av | Avion.objects.filter(oaci__iexact=avion)
			av=Accident.objects.filter(id_avion__in=comp)
			liste= liste & av
		
		#menu déroulant : nature du vol
		if 'nature' in request.GET.keys():
			nature=request.GET.getlist('nature') #getlist car possible d'en sélectionner plusieurs
			if len(nature)!=1 or nature[0]!='':
				nat=Accident.objects.filter(nature__in=nature)
				liste= liste & nat				
		
		#menu déroulant : phase de vol
		if 'phase' in request.GET.keys():
			phase=request.GET.getlist('phase') #getlist car possible d'en sélectionner plusieurs
			if len(phase)!=1 or phase[0]!='':
				pha=Accident.objects.filter(phase_de_vol__in=phase)
				liste= liste & pha
		
		#menu déroulant : dégats
		if 'degats' in request.GET.keys():
			degats=request.GET.getlist('degats') #getlist car possible d'en sélectionner plusieurs
			if len(degats)!=1 or degats[0]!='':
				deg=Accident.objects.filter(degats__in=degats)
				liste= liste & deg
		
		#menu déroulant : statut
		statut=request.GET['statut']
		if statut != '':
			sta=Accident.objects.filter(statut=statut)
			liste= liste & sta			
		
		## Nb décès ou occupants (min et max)
		if 'nb_personne' in request.GET.keys():
			nb_personne=request.GET['nb_personne']
			if nb_personne=='nb_deces':
			
				nb_min=request.GET['nb_min']
				if not nb_min=='' :
					liste=liste.filter(nb_deces__gte=nb_min)
					
				nb_max=request.GET['nb_max']
				if not nb_max=='':
					liste=liste.filter(nb_deces__lte=nb_max)

			if nb_personne=='nb_occupants':

				nb_min=request.GET['nb_min']
				if not nb_min=='' :
					liste=liste.filter(nb_occupants__gte=nb_min)
					
				nb_max=request.GET['nb_max']
				if not nb_max=='':
					liste= liste.filter(nb_occupants__lte=nb_max)
		
		## Date et heure (min et max)
		date_min=request.GET['date_min']
		if not date_min=='':
			liste = liste.filter(time__gte=datetime.datetime.strptime(date_min,"%Y-%m-%d"))
		
		date_max=request.GET['date_max']
		if not date_max=='':
			liste = liste.filter(time__lte=datetime.datetime.strptime(date_max,"%Y-%m-%d"))

		hmin=request.GET['hmin']
		if not hmin=='':
			liste = liste.filter(time__gte=datetime.datetime.strptime(hmin,"%H:%M"))
		
		hmax=request.GET['hmax']
		if not hmax=='':
			liste = liste.objects.filter(time__lte=datetime.datetime.strptime(hmax,"%H:%M"))

	###### Affichage des figures ######
	if 'aff_graphe' in request.GET.keys():
		fig=request.GET['graphe']
		bool_fig=True
		
		### Pie chart
		if fig=='Phase':	
			pie=liste.values('phase_de_vol').annotate(compt=Count('phase_de_vol'))	
			pie_chart(pie,'leur phase de vol','phase_de_vol')

		if fig=='Statut':	
			pie=liste.values('statut').annotate(compt=Count('statut'))	
			pie_chart(pie,"le statut de l'enquête",'statut')
		
		if fig=='Degats':	
			pie=liste.values('degats').annotate(compt=Count('degats'))	
			pie_chart(pie,'les dégats occasionnés','degats')
		
		### Histogramme
		if fig=='Nature':	
			bar=liste.values('nature').annotate(compt=Count('nature'))	
			bar_h(bar,'la nature du vol','nature')
	
	#### Tri des accidents ####
	tri=request.GET['tri']
	ordre=request.GET['ordre']
	if ordre=='desc': tri='-'+tri
	
	return render(request, 'accident.tmpl', 
		{                                          
        	'accident': liste.order_by(tri),
       	   	'nb': liste.count(),
	   	    'rien': liste.count()==0,
			'bool_fig': bool_fig
	   	})



##########################

""" Fonctions pour la création des pie chart""" 
def pie_chart(pie,titre,col):
	f = plt.figure()
	
	labels=[]
	sizes=[]
	for i in range(len(pie)):
		labels.append(pie[i][col])
		sizes.append(pie[i]['compt'])
	
	plt.pie(sizes, labels=labels,autopct='%1.1f%%',pctdistance=0.7)
	plt.title(f'Répartition des accidents selon {titre}',fontdict={'weight':'bold'}, pad=20)
	plt.axis('equal')

	f.savefig('monappli/static/graphe.png')
	plt.close(f)  	

""" Fonctions pour la création des histogrammes horizontaux""" 
def bar_h(bar,titre,col):
	f = plt.figure()
	
	labels=[]
	sizes=[]
	for i in range(len(bar)):
		labels.append(bar[i][col])
		sizes.append(bar[i]['compt'])
	
	plt.barh(y=labels, width=sizes, height=1)
	plt.title(f'Répartition des accidents selon {titre}',fontdict={'weight':'bold'}, pad=20)
	
	f.savefig('monappli/static/graphe.png')
	plt.close(f) 

""" Fonctions pour la création des histogrammes verticaux""" 
def bar(bar,titre,col):
	f = plt.figure()
	
	labels=[]
	sizes=[]
	for i in range(len(bar)):
		labels.append(bar[i][col])
		sizes.append(bar[i]['compt'])
	
	plt.barh(y=labels, width=sizes, height=1)
	plt.title(f"Nombre d'accidents en fonction de l'année",fontdict={'weight':'bold'}, pad=20)
	
	f.savefig('monappli/static/graphe.png')
	plt.close(f) 
