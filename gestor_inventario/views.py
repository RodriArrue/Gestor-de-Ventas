from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Producto
from.serializer import ProductoSerializer
from .permissions import esAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .permissions import esAdmin

# Create your views here.

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().select_related()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated, esAdmin]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = ProductoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework import viewsets, permissions
from .models import Pedido
from gestor_inventario.serializer import PedidoSerializer

class IsAdminOrVendedor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'vendedor']

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:  # Solo admins pueden modificar o eliminar
            return [IsAdmin()]
        return [IsAdminOrVendedor()]  # Vendedores pueden crear pedidos, admins pueden ver todos
