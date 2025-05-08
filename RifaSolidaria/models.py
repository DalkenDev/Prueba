from django.db import models
from django.forms import ValidationError
from django.db.models.functions import Now
from datetime import date

class Rifa(models.Model):
    ESTADO_OPCIONES = [
        ("oculta", "Oculta"),
        ("disponible", "Disponible"),
        ("finalizada", "Finalizada"),
        ("anulada","Anulada"),
    ]
    nombre_rifa = models.CharField(max_length = 200, verbose_name = "Nombre de Rifa")
    descripcion_rifa = models.CharField(max_length = 1000, verbose_name = "Descripcion de Rifa")
    cantidad_numeros = models.PositiveIntegerField(verbose_name = "Cantidad de números de la rifa")
    fecha_inicio_rifa = models.DateField(verbose_name = "Fecha de inicio de rifa")
    fecha_termino_rifa = models.DateField(verbose_name = "Fecha de termino de rifa")
    imagen_logo_rifa = models.ImageField(upload_to='static/images/Logos_rifa')
    estado_rifa = models.CharField(
        max_length=50,
        choices=ESTADO_OPCIONES,
        default="Disponible",
    )
    
class NumerosComprados(models.Model):
    PAGADO = "pagado"
    RESERVADO = "reservado"
    ESTADO_OPCIONES = [
        (PAGADO, "PAGADO"),
        (RESERVADO, "RESERVADO"),
    ]
    numero_comprado = models.PositiveIntegerField()
    rifa_participante = models.ForeignKey(Rifa, on_delete = models.CASCADE)
    nombre_persona = models.CharField(max_length = 50, verbose_name = "Nombre del comprador")
    apellido_persona = models.CharField(max_length = 50, verbose_name = "Apellido del comprador")
    telefono_persona = models.CharField(max_length = 14,verbose_name = "Telefono del comprador",blank=True,null=True)
    correo_persona = models.CharField(max_length = 50,verbose_name = "Correo del comprador",blank=True,null=True)  
    estado_compra_numero = models.CharField(max_length=50,verbose_name="Estado de compra del número",choices=ESTADO_OPCIONES,default=RESERVADO)


    def clean(self):
        if self.numero_comprado < 1 or self.numero_comprado > self.rifa_participante.cantidad_numeros: 
            raise ValidationError(f"El número {self.numero_comprado} no es válido. Debe estar entre 1 y {self.rifa_participante.cantidad_numeros}.")
        if NumerosComprados.objects.filter(numero_comprado=self.numero_comprado, rifa_participante=self.rifa_participante).exists():
            raise ValidationError(f"El número {self.numero_comprado} ya ha sido comprado para esta rifa.")
        if not self.telefono_persona and not self.correo_persona: 
            raise ValidationError("debe ingresar al menos un medio de contacto.")



    @staticmethod 
    def validar_codigo_pago(codigo):
        if len(codigo) != 10 or not codigo[:3].isalpha() or not codigo[3:].isdigit():
            return False
        numeros = [int(digito) for digito in codigo[3:]]
        pares = [n for n in numeros if n % 2 == 0]
        impares = [n for n in numeros if n % 2 != 0]
        return len(pares) > len(impares)
    

class PremiosRifa(models.Model):
    nombre_rifa_premios = models.ForeignKey(Rifa, on_delete=models.CASCADE)
    imagen_premio_rifa = models.ImageField(upload_to='static/images/Premios_rifa')
    nombre_premio = models.CharField(max_length=300, verbose_name="Nombre del premio")
    descripcion_premio = models.CharField(max_length=500, verbose_name="Descripción de premio")
    premio_mayor = models.BooleanField(default=False, verbose_name="Premio Mayor")  
    ganador = models.OneToOneField('Ganador', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Ganador")

    def nombre_de_rifa(self):
        return self.nombre_rifa_premios.nombre_rifa
  
class Ganador(models.Model):
    numero_comprado = models.OneToOneField(NumerosComprados, on_delete=models.CASCADE, verbose_name="Número ganador")
    nombre_ganador = models.CharField(max_length=100, verbose_name="Nombre del ganador", blank=True, null=True)
    apellido_ganador = models.CharField(max_length=100, verbose_name="Apellido del ganador", blank=True, null=True)
    telefono_ganador = models.CharField(max_length=14, verbose_name="Teléfono del ganador", blank=True, null=True)
    correo_ganador = models.EmailField(max_length=100, verbose_name="Correo electrónico del ganador", blank=True, null=True)
    fecha_ganador = models.DateField(default=date.today, verbose_name="Fecha del premio")
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, verbose_name="Rifa asociada")


    def clean(self):
        if self.numero_comprado.estado_compra_numero != "pagado":
            raise ValidationError("El número debe estar PAGADO para ser seleccionado como ganador.")

        if self.fecha_ganador < self.rifa.fecha_inicio_rifa or self.fecha_ganador > self.rifa.fecha_termino_rifa:
            raise ValidationError("Fecha fuera del rango de la rifa")

    def save(self, *args, **kwargs):
        self.nombre_ganador = self.numero_comprado.nombre_persona
        self.apellido_ganador = self.numero_comprado.apellido_persona
        self.telefono_ganador = self.numero_comprado.telefono_persona
        self.correo_ganador = self.numero_comprado.correo_persona
        super().save(*args, **kwargs)


