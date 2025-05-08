from django.shortcuts import render, redirect
from RifaSolidaria.models import PremiosRifa, Rifa, NumerosComprados, Ganador 
import re
import random
from django.contrib import messages

def index(request):
    estado = request.GET.get('estado')  
    if estado:
        if estado == '1':
            rifas = Rifa.objects.filter(estado_rifa='disponible')
        elif estado == '2':
            rifas = Rifa.objects.filter(estado_rifa='finalizada')
        elif estado == '3':
            rifas = Rifa.objects.filter(estado_rifa='anulada')
    else:
        rifas = Rifa.objects.all()

    datos = {
        'Rifas': rifas
    }
    return render(request, 'index.html', datos)

def paginarifa(request):
        rifa_id = request.GET.get('id') 
        if rifa_id:        
   
            rifa = Rifa.objects.get(id=rifa_id)
            cantidad=rifa.cantidad_numeros 

            premio = PremiosRifa.objects.filter(nombre_rifa_premios=rifa_id)
            numeros_comprados = NumerosComprados.objects.filter(rifa_participante=rifa_id)
            

            botones = [
            {"numero": i, "comprado": numeros_comprados.filter(numero_comprado=i).exists()}
            for i in range(1, cantidad + 1)]
            
            return render(request, 'paginarifa.html', {'rifa': rifa,'Premios':premio, 'numeros':numeros_comprados, 'botones':botones })

def  pagonum(request, rifa_id):
    if request.method == "POST":
        numeros_seleccionados = request.POST.getlist('numeros') 
        rifa = Rifa.objects.get(id=rifa_id)
        return render(request, 'pagonum.html', {'numeros': numeros_seleccionados, 'rifa': rifa})


def procesar_compra(request, rifa_id):
    if request.method == "POST":
        rifa = Rifa.objects.get(id=rifa_id)
        numeros_seleccionados = request.POST.get('numeros').split(',')  
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')





        if not correo and not telefono:
            messages.error(request, "debe ingresar al menos un metodo de contacto")
            return render(request, 'pagepagos.html', {
                    'rifa': rifa,
                    'numeros': numeros_seleccionados,
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'correo': correo,
                })
        

        for numero in numeros_seleccionados:
            NumerosComprados.objects.create(
                numero_comprado=int(numero),
                rifa_participante=rifa,
                nombre_persona=nombre,
                apellido_persona=apellido,
                telefono_persona=telefono,
                correo_persona=correo,
                estado_compra_numero="RESERVADO",

            )
        rifa = Rifa.objects.all()


    
        return render(request, 'index.html', {'Rifas': rifa}) 
    
def Finalizada(request, rifa_id):

    rifa = Rifa.objects.get(id=rifa_id)
    

    ganadores = Ganador.objects.filter(rifa=rifa)
    premios = PremiosRifa.objects.filter(nombre_rifa_premios=rifa)
    

    datos = {
        'rifa': rifa,
        'ganadores': ganadores,
        'premios': premios,  
    }
    return render(request, 'Finalizada.html', datos)

        
def seleccionar_ganador(request, rifa_id):
    rifa = Rifa.objects.get(id=rifa_id)
    
    if request.method == 'POST':

        premios_disponibles = PremiosRifa.objects.filter(nombre_rifa_premios=rifa, ganador__isnull=True).order_by('id')
        if not premios_disponibles.exists():
            rifa.estado_rifa = 'finalizada'
            rifa.save()
            return render(request, 'seleccionar.html', {
                'rifa': rifa,
                'error': 'No hay más premios disponibles para adjudicar.'
            })

        numeros_pagados = NumerosComprados.objects.filter(rifa_participante=rifa, estado_compra_numero="pagado")
        if not numeros_pagados.exists():
            return render(request, 'seleccionar.html', {
                'rifa': rifa,
                'error': 'No hay números pagados para seleccionar un ganador.'
            })


        numero_ganador = random.choice(numeros_pagados)
        

        ganador = Ganador.objects.create(
            numero_comprado=numero_ganador,
            rifa=rifa
        )

    
        premio = premios_disponibles.first()
        premio.ganador = ganador
        premio.save()

        if premios_disponibles.count() > 1:
            premios_restantes = premios_disponibles[1:]  
            for premio_restante in premios_restantes:
                if numeros_pagados.exists():
                    numero_ganador = random.choice(numeros_pagados)
                    ganador_restante = Ganador.objects.create(
                        numero_comprado=numero_ganador,
                        rifa=rifa
                    )
                    premio_restante.ganador = ganador_restante
                    premio_restante.save()

        ganadores = Ganador.objects.filter(rifa=rifa).select_related('numero_comprado')
        premios = PremiosRifa.objects.filter(nombre_rifa_premios=rifa)

        context = {
            'rifa': rifa,
            'ganadores': ganadores,
            'premios': premios,
        }

        return render(request, 'seleccionar.html', context)
    

    return render(request, 'seleccionar.html', {'rifa': rifa})





      
        