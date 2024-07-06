from django.shortcuts import render, redirect

from aplicaciones.mk.models import Producto

def home(request):
    return render(request, 'theme-clean.html')

def gestion(request):
    productolist = Producto.objects.all()
    return render(request, 'gestionProductos.html', {"producto": productolist})

def redirect_to_gestion_productos(request):
    return redirect('gestionProductos')

def agregarproducto(request):
    if request.method == 'POST':
        nombre = request.POST['nombreproducto']
        descripcion = request.POST['descripcionproducto']
        precio = request.POST['precioproducto']
        foto = request.FILES.get('fotoproducto')
        talla = request.POST['tallaproducto']

        nuevo_producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            foto=foto,
            talla=talla
        )
    
    return redirect('/')


def eliminarproducto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    
    if request.method == 'POST':
        producto.delete()

        return redirect('gestionProductos')