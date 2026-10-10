# Dashboard de Vendas

Sistema web para equipes de venda externa: cadastra vendedores, produtos e clientes visitados,
registra cada venda com a forma de pagamento e a localização, e resume tudo em um painel
com indicadores, gráficos e um mapa de calor das vendas.

## Funcionalidades

- Cadastro e listagem de vendedores, produtos e clientes visitados.
- Registro de vendas com forma de pagamento (dinheiro, cartão, PIX, boleto ou transferência)
  e, opcionalmente, latitude e longitude.
- Painel com o total vendido hoje, na semana, no mês e no geral.
- Desempenho por vendedor: total vendido e ticket médio.
- Relação entre visitas e vendas realizadas.
- Mapa de calor das vendas por localização.

## Tecnologias

- Python e Django
- SQLite
- Chart.js para os gráficos
- Leaflet e Leaflet.heat para o mapa de calor

## Como rodar

1. Crie um ambiente virtual e instale o Django:

   ```bash
   pip install django
   ```

2. Crie o banco de dados:

   ```bash
   python manage.py migrate
   ```

3. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

4. Abra `http://127.0.0.1:8000/` no navegador.

## Estrutura

| Caminho | Papel |
| --- | --- |
| `core/` | Configuração do projeto Django |
| `vendas/models.py` | Vendedor, Produto, ClienteVisitado e Venda |
| `vendas/views.py` | Cadastros, listagens, painel e dados do mapa |
| `vendas/forms.py` | Formulários de cadastro e de venda |
| `vendas/templates/vendas/` | Telas |

## Rotas principais

| Rota | O que mostra |
| --- | --- |
| `/` ou `/dashboard/` | Painel de indicadores |
| `/registrar/venda/` | Registro de venda |
| `/cadastrar/vendedor/`, `/cadastrar/produto/`, `/cadastrar/cliente/` | Cadastros |
| `/listar/vendedores/`, `/listar/produtos/`, `/listar/clientes/` | Listagens |
| `/mapa_calor_data/` | Dados do mapa de calor, em JSON |
