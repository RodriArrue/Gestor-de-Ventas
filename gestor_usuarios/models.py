from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        if 'role' not in extra_fields or extra_fields['role'] not in dict(CustomUser.ROLE_CHOICES):
            raise ValueError('Debe asignarse un rol válido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('vendedor', 'vendedor'),
        ('cliente', 'cliente'),
    )
    
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(Group, blank=True, related_name="custom_users_groups")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_users_permissions")
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return f"{self.email} - {self.role}"
    
    def is_admin(self):
        return self.role == 'admin'

    def is_vendedor(self):
        return self.role == 'vendedor'

    def is_cliente(self):
        return self.role == 'cliente'

# Modelo Vendedor
class Vendedor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="vendedor")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.email} - {self.nombre} {self.apellido}"

# Modelo Cliente
class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cliente")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_celular = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message="Número de celular inválido")]
    )
    direccion = models.TextField(blank=False)
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}"

# Señal para crear perfil de usuario automáticamente
@receiver(post_save, sender=CustomUser)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'vendedor':
            Vendedor.objects.create(user=instance)
        elif instance.role == 'cliente':
            Cliente.objects.create(user=instance)
    
