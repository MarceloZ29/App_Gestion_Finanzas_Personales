from django import forms
from .models import Transaccion, Categoria,MetodoPago
from .models import Presupuesto



class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        exclude = ['usuario', 'presupuesto_asociado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
            self.fields['metodo_pago'].queryset = MetodoPago.objects.filter(usuario=user)
            self.fields['metodo_pago'].empty_label = "Seleccione método de pago"

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        exclude = ['usuario']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.user)
            self.fields['metodo_pago'].queryset = MetodoPago.objects.filter(usuario=self.user)