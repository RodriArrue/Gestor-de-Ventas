from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Producto, HistorialProducto

@receiver(pre_save, sender=Producto)
def guardar_historial(sender, instance, **kwargs):
    if instance.pk:
        try:
            Producto_actual = Producto.objects.get(pk=instance.pk)
            cambios = []

            if Producto_actual.precio != instance.precio:
                cambios.append(f"Precio cambiado de ${Producto_actual.precio} ->{instance.precio}")
            if Producto_actual.stock != instance.stock:
                cambios.append(f"Stock cambiado de {Producto_actual.stock} -> {instance.stock}")

            if cambios:
                HistorialProducto.objects.create(
                    producto = instance,
                    cambio = ", ".join(cambios)
                )
        except Producto.DoesNotExist:
            pass