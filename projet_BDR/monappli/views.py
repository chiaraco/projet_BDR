from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville
from itertools import chain


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
	if not 'pays_iso' in request.GET.keys():
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
	if not 'pays_ville' in request.GET.keys(): 
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
	return render(request, 'avion.tmpl', 
	    {                                          
	        'avion': Avion.objects.all().order_by('modele'),
	        'nb': Avion.objects.count()-1,
	        'rien': Avion.objects.count()==0
	    })
	    
def compagnie(request):
	return render(request, 'compagnie.tmpl', 
	    {                                          
	        'compagnie': Compagnie.objects.all().order_by('nom_compagnie'),
	        'nb': Compagnie.objects.count()-1,
	        'rien': Compagnie.objects.count()==0
	    })

def aeroport(request):
	if not 'aero' in request.GET.keys():
		return render(request, 'aeroport.tmpl', 
		    {                                          
		        'aeroport': Aeroport.objects.all().order_by('nom_aeroport'),
		        'nb': Aeroport.objects.count()-1,
		        'rien': Aeroport.objects.count()==0
		    })
		 
	else :
		liste=Aeroport.objects.none()
		aero=request.GET['aero']
		if 'chercher_aero' in request.GET.keys():
			nom=Aeroport.objects.filter(nom_aeroport__icontains=aero)
			liste=nom
		if 'chercher_iata' in request.GET.keys():
			iata=Aeroport.objects.filter(iata__icontains=aero)
			liste=liste | iata
		if 'chercher_oaci' in request.GET.keys():
			oaci=Aeroport.objects.filter(oaci__icontains=aero)
			liste=liste | oaci
		if 'chercher_ville' in request.GET.keys():
			ville=Ville.objects.filter(nom_ville__icontains=aero)
			ae=Aeroport.objects.filter(ville__in=ville)
			liste=liste | ae
			
		return render(request, 'aeroport.tmpl', 
			{                                          
       	    	'aeroport': vi_pa.order_by('nom_aeroport'),
        	   	'nb': vi_pa.count(),
	    	    'rien': vi_pa.count()==0
	    	})
	    
def accident(request):
	return render(request, 'accident.tmpl', 
	    {                                          
	        'accident': Accident.objects.all().order_by('time'),
	        'nb': Accident.objects.count(),
	        'rien': Accident.objects.count()==0
	    })





