from django.shortcuts import render

# Create your views here.
# vendas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from .models import Vendedor, Produto, ClienteVisitado, Venda
from .forms import VendedorForm, ProdutoForm, ClienteVisitadoForm, VendaForm

# --- Views de Cadastro ---

def cadastrar_vendedor(request):
    if request.method == 'POST':
        form = VendedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_vendedores') # Redireciona após o cadastro
    else:
        form = VendedorForm()
    return render(request, 'vendas/form_cadastro.html', {'form': form, 'titulo': 'Cadastrar Vendedor'})

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'vendas/form_cadastro.html', {'form': form, 'titulo': 'Cadastrar Produto'})

def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteVisitadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteVisitadoForm()
    return render(request, 'vendas/form_cadastro.html', {'form': form, 'titulo': 'Cadastrar Cliente Visitado'})

# --- View de Registro de Vendas ---

def registrar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # Redireciona para o dashboard ou uma página de sucesso
    else:
        form = VendaForm()
    return render(request, 'vendas/registrar_venda.html', {'form': form, 'titulo': 'Registrar Nova Venda'})

# --- Views de Listagem (para referência e navegação) ---

def listar_vendedores(request):
    vendedores = Vendedor.objects.all()
    return render(request, 'vendas/lista_vendedores.html', {'vendedores': vendedores, 'titulo': 'Lista de Vendedores'})

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'vendas/lista_produtos.html', {'produtos': produtos, 'titulo': 'Lista de Produtos'})

def listar_clientes(request):
    clientes = ClienteVisitado.objects.all()
    return render(request, 'vendas/lista_clientes.html', {'clientes': clientes, 'titulo': 'Lista de Clientes Visitados'})

# --- Views de Relatórios / Métricas ---

def dashboard(request):
    # Total de vendas por período
    hoje = timezone.now().date()
    inicio_semana = hoje - timezone.timedelta(days=hoje.weekday()) # Monday
    inicio_mes = hoje.replace(day=1)

    vendas_hoje = Venda.objects.filter(data_hora__date=hoje).aggregate(total=Sum('valor_total'))['total'] or 0
    vendas_semana = Venda.objects.filter(data_hora__date__gte=inicio_semana).aggregate(total=Sum('valor_total'))['total'] or 0
    vendas_mes = Venda.objects.filter(data_hora__date__gte=inicio_mes).aggregate(total=Sum('valor_total'))['total'] or 0
    total_geral_vendas = Venda.objects.aggregate(total=Sum('valor_total'))['total'] or 0

    # Ticket médio por vendedor
    ticket_medio_vendedores = Vendedor.objects.annotate(
        ticket_medio=Avg('vendas__valor_total')
    ).order_by('-ticket_medio')

    # Ranking dos melhores vendedores (total de vendas)
    ranking_vendedores = Vendedor.objects.annotate(
        total_vendas=Sum('vendas__valor_total')
    ).order_by('-total_vendas')[:5] # Top 5

    # Conversão: visitas x vendas (simplificado, precisa de um campo de "visitas" nos modelos)
    # Para uma conversão mais precisa, precisaríamos registrar as "visitas" explicitamente.
    # Por enquanto, vamos considerar uma venda como uma "conversão de visita".
    total_visitas = ClienteVisitado.objects.count() # Número de clientes visitados = total de visitas
    total_vendas_contagem = Venda.objects.count()

    conversao = 0
    if total_visitas > 0:
        conversao = (total_vendas_contagem / total_visitas) * 100

    context = {
        'total_vendas_hoje': vendas_hoje,
        'total_vendas_semana': vendas_semana,
        'total_vendas_mes': vendas_mes,
        'total_geral_vendas': total_geral_vendas,
        'ticket_medio_vendedores': ticket_medio_vendedores,
        'ranking_vendedores': ranking_vendedores,
        'conversao': f"{conversao:.2f}%",
        'titulo': 'Dashboard de Vendas'
    }
    return render(request, 'vendas/dashboard.html', context)

# --- Mapa de Calor por Região (Exemplo - Requer JS e dados de localização) ---
# Esta view só irá retornar dados. A visualização do mapa será no template com JS.
def mapa_calor_data(request):
    # Coleta todas as vendas que possuem coordenadas de latitude e longitude
    vendas_com_local = Venda.objects.filter(latitude__isnull=False, longitude__isnull=False).values('latitude', 'longitude', 'valor_total')
    
    # Formata os dados para serem facilmente consumidos por uma biblioteca de mapa (ex: Leaflet.js, Google Maps API)
    data = []
    for venda in vendas_com_local:
        data.append({
            'lat': float(venda['latitude']),
            'lng': float(venda['longitude']),
            'value': float(venda['valor_total']) # Pode ser peso, valor, etc.
        })
    
    from django.http import JsonResponse
    return JsonResponse(data, safe=False)