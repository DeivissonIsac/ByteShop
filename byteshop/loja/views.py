from django.shortcuts import render, redirect
from .models import *
from .utils import filtrar_produtos, filtrar_min_max, ordernar_produtos, form_filtrar_produtos
import uuid
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrar_produtos(produtos, filtro)

    if request.method == "POST":
        dados = request.POST.dict()
        produtos = form_filtrar_produtos(produtos, dados)

    minimo, maximo = filtrar_min_max(produtos)
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list("tamanho", flat=True).distinct()

    ordem = request.GET.get("ordem", "MaisVendidos")
    produtos = ordernar_produtos(produtos, ordem)

    context = {"produtos": produtos, "tamanhos": tamanhos, "maximo": maximo, "minimo": minimo}
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
        novo_item = dados.get("novo_item")
        if not tamanho:
            return redirect('ver_produto', id_produto=id_produto, id_cor=id_cor)

        #identificando se um novo item está sendo adicionado ou se está aumentando a quantidade
        if novo_item == "True":
            resposta = redirect('ver_produto', id_produto=id_produto, id_cor=id_cor)
            messages.success(request, "Item adicionado no carrinho com sucesso!", "success")
        else:
            resposta = redirect('carrinho')

        #Pegar Cliente
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            #Criando Usuário Anonimo quando colocar um produto no carrinho
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
            else:
                id_sessao = str(uuid.uuid4())
                resposta.set_cookie(key="id_sessao", value=id_sessao, max_age=3600 * 24 * 30)
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)

        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, pedido = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save()
        return resposta
    else:
        return redirect('loja')


def remover_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        excluir_item = request.POST.get("form_excluir")
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect('ver_produto', id_produto=id_produto, id_cor=id_cor)
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, pedido = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        if excluir_item == "excluir_unidades":
            item_pedido.quantidade -= 1
            item_pedido.save()
            if item_pedido.quantidade <= 0:
                item_pedido.delete()
                messages.success(request, "Item removido do carrinho!", "danger")
        elif excluir_item == "excluir_item":
            item_pedido.delete()
            messages.success(request, "Item removido do carrinho!", "danger")
        return redirect('carrinho')
    else:
        return redirect('loja')

def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {"itens_pedido": None, "pedido": None}
            return render(request, 'carrinho.html', context)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = {"itens_pedido": itens_pedido, "pedido": pedido}
    return render(request, 'carrinho.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect('loja')
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {"pedido": pedido, "enderecos": enderecos, "itens_pedido": itens_pedido}
    return render(request, 'checkout.html', context)

def adicionar_endereco(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        dados = request.POST.dict()
        print(dados)
        endereco = Endereco.objects.create(
            cliente=cliente,
            rua=dados.get("rua"),
            bairro=dados.get("bairro"),
            numero=dados.get("numero"),
            complemento=dados.get("complemento"),
            cidade=dados.get("cidade"),
            estado=dados.get("estado"),
            cep=dados.get("cep")
        )
        endereco.save()
        return redirect('checkout')
    else:
        return render(request, 'adicionar_endereco.html')


def fazer_login(request):
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == "POST":
        dados = request.POST.dict()
        if dados["email"] and dados["senha"]:
            email = dados.get("email")
            senha = dados.get("senha")
            usuario = authenticate(request, username=email, password=senha)
            if usuario:
                login(request, usuario)
                messages.success(request, "Login feito com sucesso!")
                return redirect('loja')
            else:
                messages.error(request, "E-mail/Senha inválidos.", "danger")
                return redirect('fazer_login')
        else:
            messages.error(request, "E-mail/Senha inválidos.", "danger")
            return redirect('fazer_login')
    else:
        return render(request, 'user/login.html')


def criar_conta(request):
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == "POST":
        dados = request.POST.dict()
        if dados["email"] and dados["senha"] and dados["confirmar_senha"]:
            email = dados.get("email")
            senha = dados.get("senha")
            confirmar_senha = dados.get("confirmar_senha")
            if senha == confirmar_senha:
                usuario, criado = User.objects.get_or_create(username=email, email=email)
                if criado:
                    #Criando o Usuario
                    usuario.set_password(senha)
                    usuario.save()

                    #Fazendo o login do usuário criado
                    usuario = authenticate(request, username=email, password=senha)
                    login(request, usuario)

                    #Criando o Cliente e vinculando ele ao usuario
                    if request.COOKIES.get("id_sessao"):
                        id_sessao = request.COOKIES.get("id_sessao")
                        cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
                    else:
                        cliente, criado = Cliente.objects.get_or_create(email=email)
                    cliente.usuario = usuario
                    cliente.email = email
                    cliente.save()
                    messages.success(request, "Conta criada com sucesso!")
                    return redirect('loja')
                else:
                    messages.error(request, "E-mail já está cadastrado.", "danger")
            else:
                messages.error(request, "As senhas deve ser iguais.", "danger")
        else:
            messages.error(request, "Preencha os campos corretamente.", "danger")
            return redirect('criar_conta')
    return render(request, "user/criar_conta.html")


@login_required
def fazer_logout(request):
    logout(request)
    return redirect("fazer_login")


@login_required
def minha_conta(request):
    return render(request, 'user/minha_conta.html')

