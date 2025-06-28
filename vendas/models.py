from django.db import models

# Create your models here.
# vendas/models.py
from django.db import models
from django.utils import timezone # Para data/hora automática

class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_contratacao = models.DateField(auto_now_add=True) # Data que o vendedor foi cadastrado

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2) # Para valores monetários
    data_cadastro = models.DateTimeField(auto_now_add=True) # Data/hora do cadastro do produto

    def __str__(self):
        return f"{self.nome} (R${self.valor:.2f})"

class ClienteVisitado(models.Model):
    nome = models.CharField(max_length=200)
    contato = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    data_visita = models.DateTimeField(auto_now_add=True) # Data/hora da visita

    def __str__(self):
        return self.nome

class Venda(models.Model):
    # Relacionamentos com outros modelos
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT, related_name='vendas')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='vendas')
    cliente = models.ForeignKey(ClienteVisitado, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendas_realizadas')

    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50, choices=[
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
        ('transferencia', 'Transferência Bancária'),
    ])
    data_hora = models.DateTimeField(default=timezone.now) # Usaremos timezone.now para capturar a data/hora atual da venda

    # Campos opcionais para geolocalização
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"Venda #{self.id} - {self.produto.nome} por {self.vendedor.nome}"

    class Meta:
        ordering = ['-data_hora'] # Ordena as vendas pela data/hora mais recente por padrão