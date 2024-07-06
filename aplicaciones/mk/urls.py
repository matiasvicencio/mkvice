from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Esta es la ruta por defecto
    path('gestionProductos/', views.gestion, name='gestionProductos'),
    path('agregarproducto/', views.agregarproducto, name='agregar_producto'),
]
