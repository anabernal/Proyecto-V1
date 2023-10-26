from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from Aplicaciones.Seguridad.serializer import TokenObtainPersonalizadoSerializer

# Create your views here.

class TokenObtainPersonalizadoView(TokenObtainPairView):
    serializer_class = TokenObtainPersonalizadoSerializer