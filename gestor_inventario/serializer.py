from rest_framework import serializer
from .models import Producto

class ProductoSerializer(serializer.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'