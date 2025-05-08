
from django.contrib import admin
from django.urls import path
from RifaSolidaria import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='page_principal'),
    path('paginarifa/', views.paginarifa, name='paginarifa'),
    path('pagonum/<int:rifa_id>/', views.pagonum, name='pagonum'),
    path('procesar_compra/<int:rifa_id>/', views.procesar_compra, name='procesar_compra'),
    path('Finalizar/<int:rifa_id>/', views.Finalizada, name='finalizada'),
    path('rifa/<int:rifa_id>/seleccionar_ganador/', views.seleccionar_ganador, name='seleccionar_ganador'),

]
