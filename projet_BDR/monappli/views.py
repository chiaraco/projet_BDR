from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
#from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville

def accueil(request):
	return HttpResponse("ceci est la future page d'accueil\n")

#def nombre_deces(request):
#	reponse=HttpResponse()
#	reponse.write("<h1>Décès les plus importants</h1>")
#	reponse.write("<body><table border='1'>")
#	for ac in Accident.objects.raw('SELECT * FROM monappli_accident ORDER BY Nb_deces'):
#		reponse.write(f"<tr><td>{ac.IdAccident}</td> <td>{ac.Nb_deces}</td></tr>") 
#	reponse.write("</table></body>")
#	return reponse
