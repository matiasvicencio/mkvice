from django.contrib import admin

from aplicaciones.mk.models import *




admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
