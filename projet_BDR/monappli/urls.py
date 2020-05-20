from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
	path('donnees',views.donnees,name='donnees'),
	path('donnees/pays' , views.pays, name='pays'),
	path('donnees/compagnie' , views.compagnie, name='compagnie'),
	path('donnees/ville' , views.ville, name='ville'),
	path('donnees/avion' , views.avion, name='avion'),
	path('donnees/aeroport' , views.aeroport, name='aeroport'),
	path('donnees/accident' , views.accident, name='accident'),
	path('pie_chart',views.pie_chart,name='pie_chart'),
]
