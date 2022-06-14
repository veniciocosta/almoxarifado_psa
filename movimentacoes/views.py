import datetime
import decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, FormView, UpdateView
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .filters import ProdutoFilter, MovimentacaoFilter

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from movimentacoes.forms import ProdutoForm, MovimentacaoForm
from movimentacoes.models import Produto, Movimentacao
from django.db.models.aggregates import Avg, Min, Max, Sum

def home(request):
    # se estiver autenticado você não pode simplesmente usar o render, tem que ser um redirect
    # if request.user.is_authenticated:
    #     return redirect('movimentacoes:movimentacao_lista')  # redireciona para a view
    # else:
    return render(request, 'movimentacoes/homepage.html')


@login_required
def produto(request):
    form = ProdutoForm()
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimentacoes:produto_lista')

    context = {
        'form': form,
    }

    return render(request, 'movimentacoes/produto.html', context)


def produto_lista(request):
    produtos = Produto.objects.all().order_by('descricao')  # depois podemos trocar o all por filter e
    # filtrar
    myFilter = ProdutoFilter(request.GET, queryset=produtos)
    produtos=myFilter.qs

    context = {
        'produtos': produtos,
        'myFilter': myFilter,
    }
    return render(request, 'movimentacoes/produto_lista.html', context)


@login_required
def produto_submit(request, pk):
    produto = Produto.objects.get(id=pk)
    form = ProdutoForm(instance=produto)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('movimentacoes:produto_lista')

    context = {
        'form': form,
    }

    return render(request, 'movimentacoes/produto.html', context)


@login_required
def produto_delete(request, pk):
    produto = Produto.objects.get(id=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('movimentacoes:produto_lista')
    return render(request, 'movimentacoes/delete.html', {'obj': produto})


@login_required
def movimentacao(request):
    form = MovimentacaoForm()
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():

            quantidade = request.POST.get('quantidade')
            tipo = request.POST.get('tipo')
            produto = request.POST.get('produto')
            # print(produto, tipo, quantidade)
            obj_produto = Produto.objects.get(id=produto)

            # realiza contabilização de saldo
            if tipo == 'ENTRADA' or tipo=='DEVOLUCAO':
                obj_produto.quantidade = obj_produto.quantidade + decimal.Decimal(quantidade)
            else:
                if obj_produto.quantidade < decimal.Decimal(quantidade):
                    return render(request, 'movimentacoes/saida_errada.html')
                else:
                    obj_produto.quantidade = obj_produto.quantidade - decimal.Decimal(quantidade)

            # salva produto no bd
            obj_produto.save()
            # salva movimentação
            form.save()


            return redirect('movimentacoes:movimentacao_lista')

    context = {
        'form': form,
    }

    return render(request, 'movimentacoes/movimentacao.html', context)


def movimentacao_lista(request):
    parametro_page = request.GET.get('page', '1')
    parametro_limit = request.GET.get('limit', '10')

    if not (parametro_limit.isdigit() and int(parametro_limit) > 0):
        parametro_limit = '10'

    movimentacoes = Movimentacao.objects.all().order_by('-modified')


    myFilter = MovimentacaoFilter(request.GET, queryset=movimentacoes)
    movimentacoes = myFilter.qs

    movimentacoes_paginator = Paginator(movimentacoes, parametro_limit)


    try:
        movimentacoes = movimentacoes_paginator.page(parametro_page)
    except (EmptyPage, PageNotAnInteger):
        movimentacoes = movimentacoes_paginator.page(1)

    context = {
        'movimentacoes': movimentacoes,
        'myFilter': myFilter,
        'opcoes_limit': [10, 30, 60, 100],
        'filtro': request.GET
    }

    return render(request, 'movimentacoes/movimentacao_lista.html', context)


@login_required
def movimentacao_submit(request, pk): # edição
    movimentacao = Movimentacao.objects.get(id=pk)

    tipo_anterior = movimentacao.tipo
    qtd_anterior = movimentacao.quantidade

    produto = Produto.objects.get(id=movimentacao.produto.id)
    form = MovimentacaoForm(instance=movimentacao)

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, instance=movimentacao)
        if form.is_valid():
            form.save()

            # realiza contabilização de saldo
            if tipo_anterior == 'ENTRADA' and movimentacao.tipo == 'ENTRADA':
                produto.quantidade = produto.quantidade - qtd_anterior + movimentacao.quantidade
            elif tipo_anterior != 'ENTRADA' and movimentacao.tipo == 'ENTRADA':
                produto.quantidade = produto.quantidade + qtd_anterior + movimentacao.quantidade
            elif tipo_anterior != 'ENTRADA' and movimentacao.tipo != 'ENTRADA':
                produto.quantidade = produto.quantidade + qtd_anterior - movimentacao.quantidade
            elif tipo_anterior == 'ENTRADA' and movimentacao.tipo != 'ENTRADA':
                produto.quantidade = produto.quantidade - qtd_anterior - movimentacao.quantidade

            # salva produto no bd
            produto.save()

            return redirect('movimentacoes:movimentacao_lista')

    context = {
        'form': form,
    }

    return render(request, 'movimentacoes/movimentacao.html', context)


@login_required
def movimentacao_delete(request, pk):
    movimentacao = Movimentacao.objects.get(id=pk)
    if request.method == 'POST':
        produto = Produto.objects.get(id=movimentacao.produto.id)
        # realiza contabilização de saldo
        if movimentacao.tipo == 'ENTRADA':
            produto.quantidade = produto.quantidade - movimentacao.quantidade
        else:
            produto.quantidade = produto.quantidade + movimentacao.quantidade

        # salva produto no bd
        produto.save()
        # exclui movimentação
        movimentacao.delete()

        return redirect('movimentacoes:movimentacao_lista')

    return render(request, 'movimentacoes/delete.html', {'obj': movimentacao})
