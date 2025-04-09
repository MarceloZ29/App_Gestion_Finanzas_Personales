from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaccion, Categoria, MetodoPago, Presupuesto
from .forms import TransaccionForm
from .forms import PresupuestoForm
from core.forms import PresupuestoForm
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import decimal
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

@login_required
def dashboard(request):
    transacciones = Transaccion.objects.filter(usuario=request.user)
    
    # Convertir Decimal a float
    def decimal_to_float(value):
        return float(value) if value else 0.0
    
    total_ingresos = decimal_to_float(transacciones.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'])
    total_gastos = decimal_to_float(transacciones.filter(tipo='gasto').aggregate(Sum('monto'))['monto__sum'])
    balance = total_ingresos - total_gastos
    
    # Preparar datos para gráfico
    categorias = Categoria.objects.filter(usuario=request.user)
    gastos_por_categoria = [
        decimal_to_float(
            transacciones.filter(tipo='gasto', categoria=cat).aggregate(Sum('monto'))['monto__sum']
        )
        for cat in categorias
    ]
    
    return render(request, 'core/dashboard.html', {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'ultimas_transacciones': transacciones.order_by('-fecha')[:5],
        'categorias_labels': json.dumps([cat.nombre for cat in categorias]),
        'categorias_data': json.dumps(gastos_por_categoria)
    })

# Vista para listar transacciones
@login_required
def lista_transacciones(request):
    transacciones = Transaccion.objects.filter(usuario=request.user)
    
    # Filtros
    tipo = request.GET.get('tipo')
    if tipo in ['ingreso', 'gasto']:
        transacciones = transacciones.filter(tipo=tipo)
    
    # Resumen
    total_ingresos = transacciones.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    total_gastos = transacciones.filter(tipo='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    balance = total_ingresos - total_gastos

    return render(request, 'core/transacciones/lista.html', {
        'transacciones': transacciones,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
    })

# Vista para agregar una nueva transacción
@login_required
def agregar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST, user=request.user)  # Pasar user aquí
        if form.is_valid():  # Este if debe estar ANTES de usar form
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm(user=request.user)  # Y aquí también
    
    return render(request, 'core/transacciones/agregar.html', {'form': form})

# Vista para editar una transacción
@login_required
def editar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, id=transaccion_id, usuario=request.user)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm(instance=transaccion)

    return render(request, 'core/transacciones/editar.html', {'form': form})

# Vista para eliminar una transacción
@login_required
def eliminar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, id=transaccion_id, usuario=request.user)
    if request.method == 'POST':
        transaccion.delete()
        return redirect('lista_transacciones')

    return render(request, 'core/transacciones/eliminar.html', {'transaccion': transaccion})

# Vista para gestionar presupuestos

@login_required
def lista_presupuestos(request):
    presupuestos = Presupuesto.objects.filter(usuario=request.user)
    total_presupuestado = presupuestos.aggregate(Sum('monto_limite'))['monto_limite__sum']
    
    return render(request, 'core/presupuestos/lista.html', {
        'presupuestos': presupuestos,
        'total_presupuestado': total_presupuestado,
    })
# Vista para agregar un nuevo presupuesto
@login_required
def agregar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, user=request.user)  # Pasar user
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.save()
            return redirect('lista_presupuestos')
    else:
        form = PresupuestoForm(user=request.user)  # Pasar user
    
    return render(request, 'core/presupuestos/agregar.html', {'form': form})
# Vista para editar un presupuesto
@login_required
def editar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, usuario=request.user)
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            return redirect('lista_presupuestos')
    else:
        form = PresupuestoForm(instance=presupuesto)

    return render(request, 'core/presupuestos/editar.html', {'form': form})

# Vista para eliminar un presupuesto
@login_required
def eliminar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, usuario=request.user)
    if request.method == 'POST':
        presupuesto.delete()
        return redirect('lista_presupuestos')

    return render(request, 'core/presupuestos/eliminar.html', {'presupuesto': presupuesto})