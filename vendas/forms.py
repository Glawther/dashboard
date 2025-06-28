# vendas/forms.py
from django import forms
from .models import Vendedor, Produto, ClienteVisitado, Venda

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nome', 'email', 'telefone'] # Campos que aparecerão no formulário

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'valor']

class ClienteVisitadoForm(forms.ModelForm):
    class Meta:
        model = ClienteVisitado
        fields = ['nome', 'contato', 'telefone', 'endereco']

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        # Para a geolocalização, latitude e longitude serão preenchidas via JS no frontend
        fields = ['vendedor', 'produto', 'cliente', 'valor_total', 'forma_pagamento', 'latitude', 'longitude']
        widgets = {
            # Oculta os campos de lat/long no formulário, eles serão preenchidos via JS
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }