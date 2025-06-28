# vendas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Cadastro
    path('cadastrar/vendedor/', views.cadastrar_vendedor, name='cadastrar_vendedor'),
    path('cadastrar/produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('cadastrar/cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    
    # Rotas de Listagem
    path('listar/vendedores/', views.listar_vendedores, name='listar_vendedores'),
    path('listar/produtos/', views.listar_produtos, name='listar_produtos'),
    path('listar/clientes/', views.listar_clientes, name='listar_clientes'),

    # Rotas de Venda
    path('registrar/venda/', views.registrar_venda, name='registrar_venda'),

    # Rotas de Relatórios/Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mapa_calor_data/', views.mapa_calor_data, name='mapa_calor_data'), # API para dados do mapa

    # Página inicial (opcional, redireciona para o dashboard)
    path('', views.dashboard, name='home'),
]