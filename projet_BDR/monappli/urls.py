from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
	path('Deces/',views.nombre_deces,name='nombre_deces'),
	#re_path(r'^sum/(\d+)/(\d+)$' , views.mavue, name='mavue'),
]
