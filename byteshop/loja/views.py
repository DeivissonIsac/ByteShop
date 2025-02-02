from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')


def loja(request):
    return render(request, 'loja.html')


def carrinho(request):
    return render(request, 'carrinho.html')


def checkout(request):
    return render(request, 'checkout.html')


def minha_conta(request):
    return render(request, 'user/minha_conta.html')


def login(request):
    return render(request, 'user/login.html')
