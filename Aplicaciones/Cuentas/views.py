from _decimal import InvalidOperation, Decimal

from django.shortcuts import render
from psycopg2._psycopg import Float
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView
from .models import Ciudad, Persona, Cliente, CuentaBancaria, Movimiento
from .serializers import *


# Create your views here.

# Vistas relacionadas a Ciudad:
class consultarAlterarCiudadView(viewsets.ModelViewSet):
    serializer_class = ciudadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Ciudad.objects.all()
    permission_classes = [IsAuthenticated]


##################################################################################################################
# Vistas relacionadas a Persona
class consultarAlterarPersonaView(viewsets.ModelViewSet):
    serializer_class = personaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Persona.objects.all()


# Vistas relacionadas a Cliente
class consultarAlterarClienteView(viewsets.ModelViewSet):
    serializer_class = clienteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()


# Vistas relacionadas a Cta Bancaria

class consultarAlterarCtaBancariaView(viewsets.ModelViewSet):
    serializer_class = ctaBancariaSerializer
    permission_classes = [IsAuthenticated]
    queryset = CuentaBancaria.objects.all()


# Vistas relacionadas a Movimiento
class consultarAlterarMovimientoView(viewsets.ModelViewSet):
    serializer_class = movimientoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Movimiento.objects.all()


class TransferenciasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        monto = request.data.get('monto')

        # validaciones
        if not all([nro_cuenta_origen, nro_cuenta_destino, monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            monto = float(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a transferir es invalido'}, status.HTTP_400_BAD_REQUEST)

        cuenta_origen = CuentaBancaria.objects.get(nroCuenta=nro_cuenta_origen)
        cuenta_destino = CuentaBancaria.objects.get(nroCuenta=nro_cuenta_destino)
        if (cuenta_origen.moneda != cuenta_destino.moneda):
            return Response({'error', 'Cuentas deben ser de la misma moneda'}, status.HTTP_400_BAD_REQUEST)

        if (cuenta_origen.estado == 'BLOQUEADO'):
            return Response({'error', 'Cuenta origen esta bloqueada'}, status.HTTP_400_BAD_REQUEST)

        if (cuenta_destino.estado == 'BLOQUEADO'):
            return Response({'error', 'Cuenta Destino esta bloqueada'}, status.HTTP_400_BAD_REQUEST)

        if (cuenta_origen.saldo < monto):
            return Response({'error', 'Saldo insuficiente'}, status.HTTP_400_BAD_REQUEST)

        # realizar la transferencia
        saldo_anterior_origen = cuenta_origen.saldo
        saldo_anterior_destino = cuenta_destino.saldo
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto

        cuenta_origen.save()
        cuenta_destino.save()

        # registrar movimiento
        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipoMovimiento='DEB',
                                  saldoAnterior=saldo_anterior_origen,
                                  saldoActual=cuenta_origen.saldo,
                                  montoMovimiento=monto,
                                  cuentaOrigen=nro_cuenta_origen,
                                  cuentaDestino=nro_cuenta_destino,
                                  canal='APP')
        Movimiento.objects.create(cuenta=cuenta_destino,
                                  tipoMovimiento='CRED',
                                  saldoAnterior=saldo_anterior_destino,
                                  saldoActual=cuenta_destino.saldo,
                                  montoMovimiento=monto,
                                  cuentaOrigen=nro_cuenta_origen,
                                  cuentaDestino=nro_cuenta_destino,
                                  canal='APP')

        return Response({'message', 'Transferencia realizada con exito'}, status.HTTP_200_OK)


class DepositoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_destino = request.data.get('nro_cuenta_destino')
        monto = request.data.get('monto')

        # validaciones
        if not all([nro_cuenta_destino, monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            monto = float(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a depositar es invalido'}, status.HTTP_400_BAD_REQUEST)

        cuenta_destino = CuentaBancaria.objects.get(nroCuenta=nro_cuenta_destino)
        if (cuenta_destino.estado == 'BLOQUEADO'):
            return Response({'error', 'La cuenta esta Bloqueada'}, status.HTTP_400_BAD_REQUEST)

        # registrar movimiento
        Movimiento.objects.create(cuenta=cuenta_destino,
                                  tipoMovimiento='DEP',
                                  saldoAnterior=cuenta_destino.saldo,
                                  saldoActual= cuenta_destino.saldo + monto,
                                  montoMovimiento=monto,
                                  cuentaOrigen=cuenta_destino,
                                  cuentaDestino=cuenta_destino,
                                  canal='APP')
        cuenta_destino.saldo += monto
        cuenta_destino.save()
        return Response({'message', 'Deposito realizado con exito'}, status.HTTP_200_OK)



class RetiroView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nro_cuenta_origen = request.data.get('nro_cuenta_origen')
        monto = request.data.get('monto')

        # validaciones
        if not all([nro_cuenta_origen, monto]):
            return Response({'error': 'La solicitud no contiene los datos necesarios'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            monto = float(monto)
        except InvalidOperation:
            return Response({'error', 'El monto a retirar es invalido'}, status.HTTP_400_BAD_REQUEST)


        cuenta_origen = CuentaBancaria.objects.get(nroCuenta=nro_cuenta_origen)


        if (cuenta_origen.saldo < monto):
            return Response({'error', 'Saldo insuficiente para retirar el monto ingresado'}, status.HTTP_400_BAD_REQUEST)

        if (cuenta_origen.estado == 'BLOQUEADO'):
            return Response({'error', 'Cuenta Bloqueada'}, status.HTTP_400_BAD_REQUEST)

        # realizar el retiro
        saldo_anterior = cuenta_origen.saldo
        cuenta_origen.saldo -= monto
        cuenta_origen.save()

        # registrar movimiento
        Movimiento.objects.create(cuenta=cuenta_origen,
                                  tipoMovimiento='RET',
                                  saldoAnterior=saldo_anterior,
                                  saldoActual= cuenta_origen.saldo,
                                  montoMovimiento=monto,
                                  cuentaOrigen=nro_cuenta_origen,
                                  cuentaDestino=nro_cuenta_origen,
                                  canal='APP')

        return Response({'message', 'Retiro realizado con exito'}, status.HTTP_200_OK)
















