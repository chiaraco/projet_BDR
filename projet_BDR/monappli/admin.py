from django.contrib import admin

# Register your models here.

from .models import Aeroport,Compagnie,Avion,Accident,Pays,Ville

admin.site.register(Aeroport)
admin.site.register(Compagnie)
admin.site.register(Avion)
admin.site.register(Accident)
admin.site.register(Pays)
admin.site.register(Ville)

