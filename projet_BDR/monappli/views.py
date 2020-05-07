from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville

def accueil(request):
	return HttpResponse("ceci est la future page d'accueil\n")

def nombre_deces(request):
	reponse=HttpResponse()
	reponse.write("<h1>Décès les plus importants</h1>")
	reponse.write("<body><table border='1'>")
	for ac in Accident.objects.raw('SELECT * FROM monappli_accident WHERE nb_deces>0 ORDER BY nb_deces DESC' ):
		reponse.write(f"<tr><td>{ac.id_accident}</td> <td>{ac.nb_deces}</td></tr>") 
	reponse.write("</table></body>")
	return reponse
