from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from aplicaciones.mk.models import Producto, Cliente, DetalleOrden, Orden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import ProductoForm

def producto_detalle(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'home.html', {'producto': producto})

@login_required
def gestion(request):
    productolist = Producto.objects.all()
    return render(request, 'gestionProductos.html', {"producto": productolist})




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

@login_required
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


        cliente, created = Cliente.objects.get_or_create(
            rut=rut,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'email': correo,
                'telefono': telefono,
                'direccion': direccion,
            }
        )


        if not created:
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.email = correo
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.save()

        orden = Orden(cliente=cliente, total=0)
        orden.save()

        carrito = request.session.get('carrito', {})
        total_carrito = 0

        for producto_id, item in carrito.items():
            producto = get_object_or_404(Producto, id=producto_id)
            subtotal_producto = producto.precio * item['cantidad']
            total_carrito += subtotal_producto

            detalle = DetalleOrden(orden=orden, producto=producto, cantidad=item['cantidad'])
            detalle.save()

        orden.total = total_carrito
        orden.save()

        del request.session['carrito']

        return redirect('confirmacion')

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
    producto_id = request.POST.get('producto_id')
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.cantidad_disponible <= 0:
        return HttpResponse('Producto agotado.', status=400)


    if 'carrito' not in request.session:
        request.session['carrito'] = {}
    
    carrito = request.session['carrito']
    
    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] < producto.cantidad_disponible:
            carrito[producto_id]['cantidad'] += 1
        else:
            return HttpResponse('No se puede agregar más de este producto.', status=400)
    else:
        carrito[producto_id] = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1,
        }
    
    request.session.modified = True
    
    return HttpResponse('Producto agregado al carrito.')

def quitar(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('carrito')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def portfolio(request):
    return render(request, 'portfolio.html')

@login_required
def administracion(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return render(request, 'administracion.html')
@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('administracion') 
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

def confirmacion(request):
    return render(request, 'confirmacion.html')


@login_required
def ordenes(request):

    ordenes = Orden.objects.select_related('cliente').prefetch_related('detalles__producto').all()

    context = {
        'ordenes': ordenes
    }
    return render(request, 'ordenes.html', context)


def editarproducto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestionProductos') 
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editarproducto.html', {'form': form})