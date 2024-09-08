from django.contrib import admin
from .models import Cliente



# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cliente, AuthorAdmin)

admin.site.site_header = 'PUBLILICAD'
admin.site.index_title = 'Panel de Control'
admin.site.site_title = "publicidad"