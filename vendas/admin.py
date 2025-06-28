from django.contrib import admin

# Register your models here.
# vendas/admin.py
from django.contrib import admin
from .models import Vendedor, Produto, ClienteVisitado, Venda

# Register your models here.
admin.site.register(Vendedor)
admin.site.register(Produto)
admin.site.register(ClienteVisitado)
admin.site.register(Venda)
