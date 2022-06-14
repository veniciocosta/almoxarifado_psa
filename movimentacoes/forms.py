from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Produto, Movimentacao

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('created', 'modifield', 'quantidade')

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'categoria': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Defaultselect example'}),
            'und_medida': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        exclude = ('created', 'modifield')

        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Defaultselect example'}),
            'tipo': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Defaultselect example'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }