from  rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Aplicaciones.Cuentas.models import Ciudad, Persona, Cliente, CuentaBancaria, Movimiento


class ciudadSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ciudad
        fields=('__all__')

class personaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Persona
        fields=('__all__')

class clienteSerializer(serializers.ModelSerializer):
    persona = serializers.SlugRelatedField(queryset=Persona.objects.all(), slug_field='nombre') 
    class Meta:
        model= Cliente
        fields=('__all__')

class ctaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model= CuentaBancaria
        fields=('__all__')

class movimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movimiento
        fields=('__all__')



class imprimirExtractoSerializer(serializers.ModelSerializer):
   
    cliente = clienteSerializer(read_only=True)  
    movimiento = serializers.StringRelatedField(many=True) 
     #cuenta = movimientoSerializer(read_only=True) 
    class Meta:
        model= CuentaBancaria
        fields=('__all__')



