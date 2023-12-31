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


#router.register(r'v1/transferencias/', TransferenciasView.as_view())

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/transferencias/', TransferenciasView.as_view()),
    path('v1/depositos/', DepositoView.as_view()),
    path('v1/retiros/', RetiroView.as_view()),
    path('authorization/', include('rest_framework.urls')),
    path('v1/historico-movimiento/<cuenta_id>/', historicoMovimientoView.as_view()),
    path('v1/imprimir-extracto/<cliente_id>/', imprimirExtractoView.as_view()),
    #path('listar-persona/', listarPersonaView.as_view()),
    #path('registrar-persona', registrarPersonaView.as_view()),
    path('buscar-persona/<kword>/', buscarPersonaView.as_view()),
    #path('modificar-persona/<pk>/', modificarPersonaView.as_view()),
    #path('listar-cuenta/', listarCuentaView.as_view()),
    #path('registrar-cuenta', registrarCuentaView.as_view()),
    path('buscar-cuenta/<kword>/', buscarCuentaView.as_view()),
    #path('modificar-cuenta/<pk>/', modificarCuentaView.as_view()),
    #path('modificar-cuenta/<pk>/', modificarCuentaView.as_view()),


]