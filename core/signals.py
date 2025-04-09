from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Categoria, MetodoPago

@receiver(post_save, sender=User)
def crear_registros_iniciales(sender, instance, created, **kwargs):
    if created:
        # Categorías predeterminadas
        categorias = ['Comida', 'Transporte', 'Vivienda', 'Entretenimiento', 'Salud']
        for nombre in categorias:
            Categoria.objects.get_or_create(usuario=instance, nombre=nombre)
        
        # Métodos de pago predeterminados
        metodos = [
            ('EFECTIVO', 'Efectivo'),
            ('QR', 'QR'),
            ('TARJETA', 'Tarjeta')
        ]
        for codigo, nombre in metodos:
            MetodoPago.objects.get_or_create(
                usuario=instance,
                nombre=codigo,
                defaults={'descripcion': f'Pago con {nombre}'}
            )