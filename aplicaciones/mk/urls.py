from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('carrito/', views.carrito, name='carrito'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('gestionProductos/', views.gestion, name='gestionProductos'),
    path('agregarproducto/', views.agregarproducto, name='agregar_producto'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('eliminarproducto/<int:id_producto>/', views.eliminarproducto, name='eliminarproducto'),
    path('vistaclientes/', views.vista_clientes, name='vista_clientes'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
        path('quitar/<int:producto_id>/', views.quitar, name='quitar'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)