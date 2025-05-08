from django.contrib import admin
from RifaSolidaria.models import Rifa, PremiosRifa, NumerosComprados, Ganador

# Register your models here.

class RifaAdmin(admin.ModelAdmin):
    list_display = ['nombre_rifa', 'descripcion_rifa', 'cantidad_numeros', 'fecha_inicio_rifa', 'fecha_termino_rifa', 'imagen_logo_rifa', 'estado_rifa']

class PremiosRifaAdmin(admin.ModelAdmin):
    list_display = ['nombre_rifa_premios', 'imagen_premio_rifa', 'nombre_premio', 'descripcion_premio','ganador']
    
class NumerosCompradosAdmin(admin.ModelAdmin):
    list_display = ['numero_comprado', 'rifa_participante', 'nombre_persona', 'apellido_persona', 'telefono_persona', 'correo_persona', 'estado_compra_numero']

class GanadorAdmin(admin.ModelAdmin):
    list_display = ['numero_comprado', 'nombre_ganador', 'apellido_ganador', 'telefono_ganador', 'correo_ganador', 'fecha_ganador', 'rifa']
    



    
admin.site.register(Ganador, GanadorAdmin)
admin.site.register(Rifa, RifaAdmin)
admin.site.register(PremiosRifa, PremiosRifaAdmin)
admin.site.register(NumerosComprados, NumerosCompradosAdmin)
