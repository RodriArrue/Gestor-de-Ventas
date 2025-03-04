from django.db import models
from django.conf import settings
from gestor_usuarios.models import CustomUser
# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default = 0 )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['precio']),
        ]
    
    def __str__(self):
        return self.nombre
    
class HistorialProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name = "historial")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null=True)
    cambio = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __call__(self):
        return f"Historial de {self.producto.nombre} - {self.fecha}"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    vendedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'vendedor'})
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.vendedor.email} - {self.estado}"

class DetalleDePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE)  # Asegúrate de que Producto esté definido
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"





