from django.shortcuts import render, redirect
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


def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = {}
    tamanhos = {}
    cor_selecionada = None

    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = {item.cor for item in itens_estoque}
        if id_cor:
            itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id = id_cor)
            tamanhos = {item.tamanho for item in itens_estoque}
            cor_selecionada = Cor.objects.get(id=id_cor)
    context = {"produto": produto, "tem_estoque": tem_estoque, "cores": cores, "tamanhos": tamanhos,
               "cor_selecionada": cor_selecionada}
    return render(request, 'ver_produto.html', context)

def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('ver_produto', id_produto=id_produto, id_cor=id_cor)
        return redirect('carrinho')
    else:
        return redirect('loja')

def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = {"itens_pedido": itens_pedido, "pedido": pedido}
    return render(request, 'carrinho.html', context)


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request):
    return render(request, 'user/minha_conta.html')


def login(request):
    return render(request, 'user/login.html')
