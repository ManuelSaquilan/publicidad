from django.urls import include, path
from django.contrib.auth.decorators import login_required
from . import views
from .views import  ClientesListView\
                    ,ClientesUpdateView\
                    ,ContratoListView\
                    ,Contrato_Create\
                    ,contrato_update\
                    ,PagosListView\
                    ,pagos_create\
                    ,pagos_update\
                    ,video_list\
                    ,ClientesCreate\
                    ,Cliente_Update\
                    ,index\
                    ,busca_cliente\
                    ,pagos_delete\
                    ,get_active_sessions\

app_name = "publicidad"

urlpatterns = [
    path('clientes/',login_required(ClientesListView.as_view()), name="clientes_all"),
    path('cliente_create/',ClientesCreate.as_view(), name="cliente_create"),
    path('cliente_update/<int:pk>',Cliente_Update, name="cliente_update"),
    path('contrato/',ContratoListView.as_view(), name="contratos_list"),
    path('contrato_create/',Contrato_Create, name="contrato_create"),
    path('contrato_update/<int:pk>',contrato_update, name="contrato_update"),
    path('pagos/',PagosListView.as_view(), name="pagos_list"),
    path('pagos_create/',pagos_create, name="pagos_create"),
    path('pagos_update/<int:pk>',pagos_update, name="pagos_update"),
    path('pagos_delete/<int:pk>',pagos_delete, name="pagos_delete"),
    path('videos',video_list, name="videos"),
    path('index',index.as_view(), name="index"),
    path('ping/', views.ping_view, name='ping_view'),
    path('busca_cliente/', busca_cliente, name='busca_cliente'),
    path('sesiones/', get_active_sessions, name='sesiones_activas'),
]
