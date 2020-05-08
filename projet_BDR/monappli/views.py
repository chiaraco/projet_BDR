from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville


def accueil(request):
	return HttpResponse("ceci est la future page d'accueil\n")

def nombre_deces(request,annee1,annee2):
	reponse=HttpResponse()
	reponse.write(f"<h1>Accidents causant le plus de décès entre {annee1} et {annee2}</h1>")
	reponse.write("<body><table border='1'>")
	reponse.write(f"<tr><td>Nombre de decès</td> <td>Date</td><td>Pays</td><td>Nature du vol</td></tr>")
	for ac in Accident.objects.raw(f"SELECT * FROM monappli_accident WHERE  nb_deces>0 AND (EXTRACT(YEAR FROM time) BETWEEN {int(annee1)} AND {int(annee2)}) ORDER BY nb_deces DESC" ):
		reponse.write(f"<tr><td>{ac.nb_deces}</td> <td>{ac.time.strftime('%d/%m/%Y')}</td><td>{ac.nom_pays.nom_pays}</td><td>{ac.nature}</td></tr>") 
	reponse.write("</table></body>")
	return reponse

def donnees(request,table):

	if table=='pays':
		return render(request, 'pays.tmpl', 
			{                                          
            	'pays': Pays.objects.all().order_by('nom_pays'),
            	'nb': Pays.objects.count()-1,
		        'rien': Pays.objects.count()==0
		    })
	elif table=='ville':
		return render(request, 'ville.tmpl', 
			{                                          
            	'ville': Ville.objects.all().order_by('nom_ville'),
            	'nb': Ville.objects.count()-1,
		        'rien': Ville.objects.count()==0
		    })

	elif table=='avion':
		return render(request, 'avion.tmpl', 
		    {                                          
		        'avion': Avion.objects.all().order_by('modele'),
		        'nb': Avion.objects.count()-1,
		        'rien': Avion.objects.count()==0
		    })
	elif table=='compagnie':
		return render(request, 'compagnie.tmpl', 
		    {                                          
		        'compagnie': Compagnie.objects.all().order_by('nom_compagnie'),
		        'nb': Compagnie.objects.count()-1,
		        'rien': Compagnie.objects.count()==0
		    })
	elif table=='aeroport':
		return render(request, 'aeroport.tmpl', 
		    {                                          
		        'aeroport': Aeroport.objects.all().order_by('nom_aeroport'),
		        'nb': Aeroport.objects.count()-1,
		        'rien': Aeroport.objects.count()==0
		    })
	elif table=='accident':
		return render(request, 'accident.tmpl', 
		    {                                          
		        'accident': Accident.objects.all().order_by('time'),
		        'nb': Accident.objects.count(),
		        'rien': Accident.objects.count()==0
		    })

