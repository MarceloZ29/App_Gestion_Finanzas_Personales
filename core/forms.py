from django import forms
from .models import Transaccion
from .models import Presupuesto

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion', 'usuario', 'categoria', 'metodo_pago'] 


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['usuario', 'monto_limite', 'fecha_inicio', 'fecha_fin', 'categoria', 'metodo_pago']