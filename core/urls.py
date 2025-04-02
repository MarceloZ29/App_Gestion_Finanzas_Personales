from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #urlsTransacciones
    path('transacciones/', views.lista_transacciones, name='lista_transacciones'),
    path('transacciones/agregar/', views.agregar_transaccion, name='agregar_transaccion'),
    path('transacciones/editar/<int:transaccion_id>/', views.editar_transaccion, name='editar_transaccion'),
    path('transacciones/eliminar/<int:transaccion_id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    #urlsPresupuestos
    path('presupuestos/', views.lista_presupuestos, name='lista_presupuestos'),
    path('presupuestos/agregar/', views.agregar_presupuesto, name='agregar_presupuesto'),
    path('presupuestos/editar/<int:presupuesto_id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:presupuesto_id>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
