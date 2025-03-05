import django_filters
from .models import Pedido

class PedidoFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr="gte")
    fecha_fin = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr="lte")
    vendedor = django_filters.CharFilter(field_name="vendedor__email", lookup_expr="icontains")

    class Meta:
        model = Pedido
        fields = ['fecha_inicio', 'fecha_fin', 'vendedor']
