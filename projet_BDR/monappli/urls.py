from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
	re_path(r'^deces/([0-9]{4})-([0-9]{4})$',views.nombre_deces,name='nombre_deces'),
	path('donnees',views.donnees,name='donnees'),
	path('donnees/pays' , views.pays, name='pays'),
	path('donnees/compagnie' , views.compagnie, name='compagnie'),
	path('donnees/ville' , views.ville, name='ville'),
	path('donnees/avion' , views.avion, name='avion'),
	path('donnees/aeroport' , views.aeroport, name='aeroport'),
	path('donnees/accident' , views.accident, name='accident'),
]
