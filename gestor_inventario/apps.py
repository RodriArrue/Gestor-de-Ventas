from django.apps import AppConfig



class GestorInventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestor_inventario'

    def ready(self):
        import gestor_inventario.signals