from django.contrib import admin
from .models import Categoria, MetodoPago, Transaccion, Presupuesto, PresupuestoTransaccion, Reporte, Notificacion, ConfiguracionUsuario, RegistroSesion

# Registrar los modelos
admin.site.register(Categoria)
admin.site.register(MetodoPago)
admin.site.register(Transaccion)
admin.site.register(Presupuesto)
admin.site.register(PresupuestoTransaccion)
admin.site.register(Reporte)
admin.site.register(Notificacion)
admin.site.register(ConfiguracionUsuario)
admin.site.register(RegistroSesion)
