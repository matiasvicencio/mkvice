from django.db import models
from django.core.validators import RegexValidator


telefono_validator = RegexValidator(regex=r'^\d{9,15}$', message="El número de teléfono debe contener entre 9 y 15 dígitos sin espacios ni guiones.")
rut_validator = RegexValidator(regex=r'^\d{8}-[\dKk]$', message="El RUT debe tener el formato 12345678-9 o 12345678-K.")

class Cliente(models.Model):
    rut = models.CharField(primary_key=True, max_length=12, validators=[rut_validator], help_text="Ingresa el RUT en el formato 12345678-9 o 12345678-K.")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, validators=[telefono_validator], help_text="Ingresa el número de teléfono sin espacios ni guiones.")
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    tallas_choices = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    talla = models.CharField(max_length=2, choices=tallas_choices)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='ordenes', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Orden de {self.cliente.nombre} - Fecha: {self.fecha}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Detalle de la orden {self.orden.id}: {self.producto.nombre} x {self.cantidad}"
