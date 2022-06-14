import django_filters
from django_filters import CharFilter, DateTimeFilter, NumberFilter

from django import forms
from .models import *


class MovimentacaoFilter(django_filters.FilterSet):
    data_inicial = DateTimeFilter(field_name='created', lookup_expr='gte', widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    data_final = DateTimeFilter(field_name='created', lookup_expr='lte', widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))
    produto = CharFilter(field_name='produto__descricao', lookup_expr='icontains')

    class Meta:
        model = Movimentacao
        fields = '__all__'
        exclude = ['created', 'modified', 'produto' , 'quantidade']


class ProdutoFilter(django_filters.FilterSet):
    descricao_produto = CharFilter(field_name='descricao', lookup_expr='icontains')
    quantidade_produto = NumberFilter(field_name='quantidade', lookup_expr='gt')
    class Meta:
        model = Produto
        fields = '__all__'
        exclude = ['created', 'modified', 'descricao', 'quantidade']