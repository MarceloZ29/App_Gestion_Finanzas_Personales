from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaccion, Categoria, MetodoPago, Presupuesto
from .forms import TransaccionForm
from .forms import PresupuestoForm
from core.forms import PresupuestoForm

# Vista principal del Dashboard
@login_required
def dashboard(request):
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'core/dashboard.html', {'transacciones': transacciones})

# Vista para listar transacciones
@login_required
def lista_transacciones(request):
    transacciones = Transaccion.objects.filter(usuario=request.user)
    return render(request, 'core/transacciones/lista.html', {'transacciones': transacciones})

# Vista para agregar una nueva transacción
@login_required
def agregar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm()
    
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
    return render(request, 'core/presupuestos/lista.html', {'presupuestos': presupuestos})
# Vista para agregar un nuevo presupuesto
@login_required
def agregar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.save()
            return redirect('lista_presupuestos')
    else:
        form = PresupuestoForm()

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