from django.shortcuts import get_object_or_404, render, redirect

from aplicaciones.mk.models import Producto



def producto_detalle(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'home.html', {'producto': producto})

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
    producto.delete()
    return redirect('gestionProductos')
    

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def carrito(request):
    return render(request, 'carrito.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def portfolio(request):
    return render(request, 'portfolio.html')