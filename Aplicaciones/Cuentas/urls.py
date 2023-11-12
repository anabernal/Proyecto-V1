from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()

router.register(r'consultarAlterarPersona',consultarAlterarPersonaView)

router.register(r'consultarAlterarCliente', consultarAlterarClienteView)

router.register(r'consultarAlterarCtaBancaria',consultarAlterarCtaBancariaView)

router.register(r'consultarAlterarCiudad',consultarAlterarCiudadView)

router.register(r'consultarAlterarMovimiento',consultarAlterarMovimientoView)

router.register(r'consultarAlterarMovimiento',consultarAlterarMovimientoView)

#router.register(r'v1/transferencias/', TransferenciasView.as_view())

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/transferencias/', TransferenciasView.as_view()),
    path('v1/depositos/', DepositoView.as_view()),
    path('v1/retiros/', RetiroView.as_view()),
    path('authorization/', include('rest_framework.urls')),

]