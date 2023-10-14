from _decimal import InvalidOperation, Decimal

from django.shortcuts import render
from psycopg2._psycopg import Float
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView,RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView,RetrieveUpdateDestroyAPIView, UpdateAPIView
from Aplicaciones.Cuentas.serializers import *
from Aplicaciones.Cuentas.models import *
# Create your views here.

#Vistas relacionadas a Ciudad:
class CiudadView(viewsets.ModelViewSet):
    serializer_class = ciudadSerializer
    queryset = Ciudad.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
class detalleCiudadView(viewsets.ModelViewSet):
    serializer_class = ciudadSerializer
    queryset = Ciudad.objects.all()

class consultarAlterarCiudadView(viewsets.ModelViewSet):
    serializer_class = ciudadSerializer
    queryset = Ciudad.objects.all()
# Vistas relacionadas a Movimiento



##################################################################################################################
#Vistas relacionadas a Persona
class PersonaView(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = personaSerializer

class detallePersonaView(viewsets.ModelViewSet):
    serializer_class = personaSerializer
    queryset = Persona.objects.all()

class consultarAlterarPersonaView(viewsets.ModelViewSet):
    serializer_class = personaSerializer
    queryset = Persona.objects.all()



# Vistas relacionadas a Cliente
class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = clienteSerializer

class detalleClienteView(viewsets.ModelViewSet):
    serializer_class = clienteSerializer
    queryset = Cliente.objects.all()

class consultarAlterarClienteView(viewsets.ModelViewSet):
    serializer_class = clienteSerializer
    queryset = Cliente.objects.all()


# Vistas relacionadas a Cta Bancaria
class CuentaView(viewsets.ModelViewSet):
    queryset = CuentaBancaria.objects.all()
    serializer_class = ctaBancariaSerializer


class detalleCtaBancariaView(viewsets.ModelViewSet):
    serializer_class = ctaBancariaSerializer
    queryset = CuentaBancaria.objects.all()

class consultarAlterarCtaBancariaView(viewsets.ModelViewSet):
    serializer_class = ctaBancariaSerializer
    queryset = CuentaBancaria.objects.all()




# Vistas relacionadas a Movimiento
class MovimientoView(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = movimientoSerializer

class detalleMovimientoView(viewsets.ModelViewSet):
    serializer_class = movimientoSerializer
    queryset = Movimiento.objects.all()

class consultarAlterarMovimientoView(viewsets.ModelViewSet):
    serializer_class = movimientoSerializer
    queryset = Movimiento.objects.all()


class TransferenciasView(APIView):
    def post(self, request):
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        nro_cuenta_destino=request.data.get('nro_cuenta_destino')
        monto= request.data.get('monto')

        #validaciones
        if not all([nro_cuenta_origen, nro_cuenta_destino,monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'}, status= status.HTTP_400_BAD_REQUEST)
        try:
            monto= float(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a transferir es invalido'}, status.HTTP_400_BAD_REQUEST)

        cuenta_origen= CuentaBancaria.objects.get(nro_cuenta=nro_cuenta_origen)
        cuenta_destino = CuentaBancaria.objects.get(nro_cuenta=nro_cuenta_destino)

        if(cuenta_origen.saldo<monto):
            return Response({'error', 'Saldo insuficiente'}, status.HTTP_400_BAD_REQUEST)

        #realizar la transferencia
        cuenta_origen.saldo -=monto
        cuenta_destino.saldo +=monto

        cuenta_origen.save()
        cuenta_destino.save()

        #registrar movimiento
        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipoMovimiento='DEB',
                                  monto_movimiento=monto,
                                  cuenta_origen=nro_cuenta_origen,
                                  cuenta_destino=nro_cuenta_destino,
                                  canal='APP')
        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipoMovimiento='CRED',
                                  monto_movimiento=monto,
                                  cuenta_origen=nro_cuenta_origen,
                                  cuenta_destino=nro_cuenta_destino,
                                  canal='APP')

        return Response({'message', 'Transferencia realizada con exito'}, status.HTTP_200_OK)




















