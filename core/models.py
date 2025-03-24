from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo MetodoPago
class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con usuario

    def __str__(self):
        return self.nombre

# Modelo Transaccion
class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Cambio a DecimalField
    fecha = models.DateField(auto_now_add=True)  # Fecha automática
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # No perder registros
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion} - {self.monto}"

# Modelo Presupuesto
class Presupuesto(models.Model):
    monto_limite = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Presupuesto de {self.usuario.username}"

# Modelo PresupuestoTransaccion
class PresupuestoTransaccion(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE)  # Una transacción solo en un presupuesto

    def __str__(self):
        return f"{self.presupuesto} - {self.transaccion}"

# Modelo Reporte
class Reporte(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_generacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.usuario.username}"

# Modelo Notificacion
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.usuario.username}"

# Modelo ConfiguracionUsuario
class ConfiguracionUsuario(models.Model):
    MONEDA_CHOICES = [
        ('USD', 'Dólares'),
        ('EUR', 'Euros'),
        ('BOB', 'Bolivianos'),
    ]
    IDIOMA_CHOICES = [
        ('ES', 'Español'),
        ('EN', 'Inglés'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES)
    idioma = models.CharField(max_length=2, choices=IDIOMA_CHOICES)

    def __str__(self):
        return f"Configuración de {self.usuario.username}"

# Modelo RegistroSesion
class RegistroSesion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()  # Cambio de CharField a IPAddressField
    navegador = models.CharField(max_length=200)

    def __str__(self):
        return f"Sesión de {self.usuario.username}"
