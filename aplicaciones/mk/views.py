from pyexpat.errors import messages
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
        cantidad = request.POST['cantidadproducto']

        nuevo_producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            foto=foto,
            talla=talla,
            cantidad=cantidad
        )
    
    return redirect('gestionProductos')


def eliminarproducto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    producto.delete()
    return redirect('gestionProductos')
    

def home(request):
    producto_destacado = Producto.objects.get(pk=9)
    productos = Producto.objects.all()
    return render(request, 'home.html', {
        'productos': productos,
        'producto_destacado': producto_destacado,
    })

def carrito(request):
    return render(request, 'carrito.html')

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    # Verificar si hay stock disponible
    if producto.cantidad_disponible <= 0:
        messages.error(request, 'Este producto está agotado.')
        return redirect('home')

    # Agregar producto al carrito
    # Aquí deberías implementar la lógica para agregar el producto al carrito

    # Reducir la cantidad disponible
    producto.cantidad_disponible -= 1
    producto.save()

    # Mensaje de éxito
    messages.success(request, 'Producto agregado al carrito.')

    return redirect('home')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def portfolio(request):
    return render(request, 'portfolio.html')