from django.shortcuts import render
from .models import *

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, categoria=None):
    produtos = Produto.objects.filter(ativo=True)
    if categoria:
        produtos = produtos.filter(categoria__nome=categoria)
    context = {"produtos": produtos}
    return render(request, 'loja.html', context)


def ver_produto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    context = {"produto": produto}
    return render(request, 'ver_produto.html', context)


def carrinho(request):
    return render(request, 'carrinho.html')


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request):
    return render(request, 'user/minha_conta.html')


def login(request):
    return render(request, 'user/login.html')
