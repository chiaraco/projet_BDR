from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
	re_path(r'^deces/([0-9]{4})-([0-9]{4})$',views.nombre_deces,name='nombre_deces'),
	re_path(r'^donnees(/?\w*)$',views.donnees,name='donnees'),
	#re_path(r'^sum/(\d+)/(\d+)$' , views.mavue, name='mavue'),
]
