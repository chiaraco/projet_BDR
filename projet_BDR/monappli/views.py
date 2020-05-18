from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville
import datetime


def accueil(request):
	return render(request,'accueil.tmpl')


def nombre_deces(request,annee1,annee2):
	reponse=HttpResponse()
	reponse.write(f"<h1>Accidents causant le plus de décès entre {annee1} et {annee2}</h1>")
	reponse.write("<body><table border='1'>")
	reponse.write(f"<tr><td>Nombre de decès</td> <td>Date</td><td>Pays</td><td>Nature du vol</td></tr>")
	for ac in Accident.objects.raw(f"SELECT * FROM monappli_accident WHERE  nb_deces>0 AND (EXTRACT(YEAR FROM time) BETWEEN {int(annee1)} AND {int(annee2)}) ORDER BY nb_deces DESC" ):
		reponse.write(f"<tr><td>{ac.nb_deces}</td> <td>{ac.time.strftime('%d/%m/%Y')}</td><td>{ac.nom_pays.nom_pays}</td><td>{ac.nature}</td></tr>") 
	reponse.write("</table></body>")
	return reponse


def donnees(request):
	return render(request,'choix_table.tmpl')

	
def pays(request):
	if not request.GET.keys():
		return render(request, 'pays.tmpl', 
			{                                          
        	    'pays': Pays.objects.all().order_by('nom_pays'),
        	    'nb': Pays.objects.count()-1,
			    'rien': Pays.objects.count()==0
			})
		 
	else :
		pays_iso=request.GET['pays_iso']
		pa_iso=Pays.objects.none()
		if 'chercher_iso' in request.GET.keys():
			iso=Pays.objects.filter(iso__icontains=pays_iso)
			pa_iso=iso
		if 'chercher_pays' in request.GET.keys():
			pa=Pays.objects.filter(nom_pays__icontains=pays_iso)
			pa_iso=pa_iso | pa
			
		return render(request, 'pays.tmpl', 
			{                                          
        	   	'pays': pa_iso.order_by('nom_pays'),
        	   	'nb': pa_iso.count(),
	    	    'rien': pa_iso.count()==0
	    	})


def ville(request):
	if not request.GET.keys(): 
		return render(request, 'ville.tmpl', 
		{                                          
           	'ville': Ville.objects.all().order_by('nom_ville'),
           	'nb': Ville.objects.count()-1,
	        'rien': Ville.objects.count()==0
	    })
	    
	else :
		vi_pa=Ville.objects.none()
		pays_ville=request.GET['pays_ville']
		if 'chercher_ville' in request.GET.keys():
			vi=Ville.objects.filter(nom_ville__icontains=pays_ville)
			vi_pa=vi
		if 'chercher_pays' in request.GET.keys():
			pays=Pays.objects.filter(nom_pays__icontains=pays_ville)
			pa=Ville.objects.filter(nom_pays__in=pays)
			vi_pa=vi_pa | pa

		return render(request, 'ville.tmpl', 
		{                                          
           	'ville': vi_pa.order_by('nom_ville'),
           	'nb': vi_pa.count(),
	        'rien': vi_pa.count()==0
	    })

		
def avion(request):
	if not request.GET.keys():
		return render(request, 'avion.tmpl', 
	    	{                                          
	        	'avion': Avion.objects.all().order_by('modele'),
	        	'nb': Avion.objects.count()-1,
	        	'rien': Avion.objects.count()==0
	    	})
	else :
		av=Avion.objects.none()
		rech_avion=request.GET['rech_avion']
		if 'chercher_modele' in request.GET.keys():
			av=Avion.objects.filter(modele__icontains=rech_avion)
		if 'chercher_iata' in request.GET.keys():
			iata=Avion.objects.filter(iata__icontains=rech_avion)
			av=av | iata
		if 'chercher_oaci' in request.GET.keys():
			oaci=Avion.objects.filter(oaci__icontains=rech_avion)
			av=av | oaci

		return render(request, 'avion.tmpl', 
		{                                          
           	'avion': av.order_by('modele'),
           	'nb': av.count(),
	        'rien': av.count()==0
	    })

	    
def compagnie(request):
	if not request.GET.keys():
		return render(request, 'compagnie.tmpl', 
	    	{                                          
	        	'compagnie': Compagnie.objects.all().order_by('nom_compagnie'),
	        	'nb': Compagnie.objects.count()-1,
	        	'rien': Compagnie.objects.count()==0
	   		})

	else :
		comp=Compagnie.objects.all()
		rech_compagnie=request.GET['rech_compagnie']
		if 'rech_compagnie' in request.GET.keys():
			comp=comp & Compagnie.objects.filter(nom_compagnie__icontains=rech_compagnie)
		if 'chercher_alias' in request.GET.keys():
			alias=Compagnie.objects.filter(alias__icontains=rech_compagnie)
			comp=comp & alias

		code=request.GET['code']
		if ('co' in request.GET.keys()) and (code!=''):
			co=request.GET['co']
			if co=='iata':
				iata=Compagnie.objects.filter(iata__iexact=code)
				comp=comp & iata				
			elif co=='oaci':
				oaci=Compagnie.objects.filter(oaci__iexact=code)
				comp=comp & oaci

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


def aeroport(request):
	if not request.GET.keys():
		return render(request, 'aeroport.tmpl', 
		    {                                          
		        'aeroport': Aeroport.objects.all().order_by('nom_aeroport'),
		        'nb': Aeroport.objects.count()-1,
		        'rien': Aeroport.objects.count()==0
		    })
		 
	else :
		liste=Aeroport.objects.all()
		aero=request.GET['aero']
		if not aero=='':
			nom=Aeroport.objects.filter(nom_aeroport__icontains=aero)
			liste=liste & nom
		
		code=request.GET['code']
		if ('co' in request.GET.keys()) and (code!=''):
			co=request.GET['co']
			if co=='iata':
				iata=Aeroport.objects.filter(iata__iexact=code)
				liste=liste & iata				
			elif co=='oaci':
				oaci=Aeroport.objects.filter(oaci__iexact=code)
				liste=liste & oaci

		if 'chercher_ville' in request.GET.keys():
			ville=Ville.objects.filter(nom_ville__icontains=vipa)
			ae=Aeroport.objects.filter(ville__in=ville)
			liste=liste & ae

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

	    
def accident(request):
	if not request.GET.keys():
		return render(request, 'accident.tmpl', 
	    	{                                          
	        	'accident': Accident.objects.all().order_by('time'),
	        	'nb': Accident.objects.count(),
	        	'rien': Accident.objects.count()==0
	   	})
	else:
		liste=Accident.objects.all()
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

		lieu=request.GET['lieu']
		if not lieu=='':
			liste_lieu=Accident.objects.filter(emplacement__icontains=lieu)

			pays=Pays.objects.filter(nom_pays__icontains=lieu)
			pa=Accident.objects.filter(nom_pays__in=pays)
			liste_lieu=liste_lieu | pa

			liste=liste & liste_lieu
		
		compagnie=request.GET['compagnie']
		if not compagnie=='':
			comp=Compagnie.objects.filter(nom_compagnie__icontains=compagnie)
			comp=comp | Compagnie.objects.filter(alias__icontains=compagnie)
			comp=comp | Compagnie.objects.filter(iata__iexact=compagnie)
			comp=comp | Compagnie.objects.filter(oaci__iexact=compagnie)
			co=Accident.objects.filter(nom_compagnie__in=comp)
			liste= liste & co

		avion=request.GET['avion']
		if not avion=='':
			av=Avion.objects.filter(modele__icontains=avion)
			av=av | Avion.objects.filter(iata__iexact=avion)
			av=av | Avion.objects.filter(oaci__iexact=avion)
			av=Accident.objects.filter(id_avion__in=comp)
			liste= liste & av

#################
		if 'nb_personne' in request.GET.keys():
			nb_personne=request.GET['nb_personne']
			if nb_personne=='nb_deces':
				acc=Accident.objects.all().exclude(nb_deces__isnull=True)
				nb_min=request.GET['nb_min']
				if not nb_min=='' :
					acc=acc & Accident.objects.filter(nb_deces__gte=nb_min)
					print(acc)
				nb_max=request.GET['nb_max']
				if not nb_max=='':
					acc= acc & Accident.objects.filter(nb_deces__lte=nb_max)
				liste= liste & acc

			if nb_personne=='nb_occupants':
				acc=Accident.objects.all().exclude(nb_occupants__isnull=True)
				print(acc)
				print(len(acc))
				nb_min=request.GET['nb_min']
				if not nb_min=='' :
					acc=acc & Accident.objects.filter(nb_occupants__gte=nb_min)
				nb_max=request.GET['nb_max']
				if not nb_max=='':
					acc= acc & Accident.objects.filter(nb_occupants__lte=nb_max)
				liste= liste & acc
#################

		date_min=request.GET['date_min']
		if not date_min=='':
			date=Accident.objects.filter(time__gte=datetime.datetime.strptime(date_min,"%Y-%m-%d"))
			liste = liste & date
		
		date_max=request.GET['date_max']
		if not date_max=='':
			date=Accident.objects.filter(time__lte=datetime.datetime.strptime(date_max,"%Y-%m-%d"))
			liste = liste & date

		hmin=request.GET['hmin']
		if not hmin=='':
			heure=Accident.objects.filter(time__gte=datetime.datetime.strptime(hmin,"%H:%M"))
			liste = liste & heure
		
		hmax=request.GET['hmax']
		if not hmax=='':
			heure=Accident.objects.filter(time__lte=datetime.datetime.strptime(hmax,"%H:%M"))
			liste = liste & heure
		return render(request, 'accident.tmpl', 
			{                                          
       	    	'accident': liste.order_by('time'),
        	   	'nb': liste.count(),
	    	    'rien': liste.count()==0
	    	})




