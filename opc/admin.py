from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(RegOpcUaServer)
admin.site.register(Dienstleistungen)
admin.site.register(Produkt)
admin.site.register(Kunden)
admin.site.register(ProduktionsAuftrag)
admin.site.register(Ressourcenplanung)
admin.site.register(Test)
admin.site.register(Serverdata)



#class AuthorAdmin(admin.ModelAdmin):
 #   list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
