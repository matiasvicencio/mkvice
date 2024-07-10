from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from aplicaciones.mk.models import Producto, Cliente, DetalleOrden, Orden
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.configuration import Configuration 

configuration = Configuration()
configuration.commerce_code = '597055555532'
configuration.api_key = 'YourAPIKey'
configuration.integration_type = IntegrationType.TEST

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


def vista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'vistaclientes.html', {'clientes': clientes})

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

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        cliente = Cliente.objects.create(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            email=correo,
            telefono=telefono,
            direccion=direccion
        )

        orden = Orden(cliente=cliente, total=0)
        orden.save()

        carrito = request.session.get('carrito', {})
        total_carrito = 0

        for producto_id, item in carrito.items():
            producto = get_object_or_404(Producto, id=producto_id)
            subtotal_producto = producto.precio * item['cantidad']
            total_carrito += subtotal_producto

            detalle = DetalleOrden(orden=orden, producto=producto, cantidad=item['cantidad'], subtotal=subtotal_producto)
            detalle.save()

        orden.total = total_carrito
        orden.save()

        del request.session['carrito']

        return redirect('pagina_de_confirmacion')  


    carrito = request.session.get('carrito', {})
    productos_carrito = []
    total_carrito = 0

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal_producto = producto.precio * item['cantidad']
        total_carrito += subtotal_producto
        productos_carrito.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': item['cantidad'],
            'foto_url': producto.foto.url
        })

    context = {
        'productos_carrito': productos_carrito,
        'total_carrito': total_carrito,
    }
    return render(request, 'carrito.html', context)


def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)
        
        if 'carrito' not in request.session:
            request.session['carrito'] = {}
        
        carrito = request.session['carrito']
        
        if producto_id in carrito:
            carrito[producto_id]['cantidad'] += 1
        else:
            carrito[producto_id] = {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': 1,
            }
        
        request.session.modified = True
        
        return HttpResponse('Producto agregado al carrito.')
    else:
        return HttpResponse('Error: Método no permitido.')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def portfolio(request):
    return render(request, 'portfolio.html')


