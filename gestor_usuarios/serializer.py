from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Vendedor, Cliente

class Userserializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'email', 'role']

class VendedorSerializer(serializers.ModelSerializer):
    user = Userserializer()

    class Meta:
        model = Vendedor
        fields = ['id', 'user', 'nombre', 'apellido']

class ClienteSerializer(serializers.ModelSerializer):
    user = Userserializer()

    class Meta:
        model = Cliente
        fields = ['id', 'user', 'nombre', 'apellido', 'numero_celular', 'direccion']