from django.db.models import Max, Min
from .models import ItemEstoque

def filtrar_produtos(produtos, filtro):
    if filtro:
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return  produtos

def filtrar_min_max(produtos):
    maximo = 0
    minimo = 0
    if produtos:
        maximo = list(produtos.aggregate(Max("preco")).values())[0]
        maximo = round(maximo, 2)
        minimo = list(produtos.aggregate(Min("preco")).values())[0]
        minimo = round(minimo, 2)
    return minimo, maximo

def form_filtrar_produtos(produtos, dados):
    if dados["preco_maximo"] == "maximo":
        produtos = produtos.filter(preco__gte=dados.get("preco_minimo"))
    else:
        produtos = produtos.filter(preco__gte=dados.get("preco_minimo"), preco__lte=dados.get("preco_maximo"))
    if "tamanho" in dados:
        itens = ItemEstoque.objects.filter(produto__in=produtos, tamanho=dados.get("tamanho"))
        id_produtos = itens.values_list("produto", flat=True).distinct()
        produtos = produtos.filter(id__in=id_produtos)
    return produtos

def ordernar_produtos(produtos, ordem):
    if ordem == "MenorPreco":
        produtos = produtos.order_by("preco")
    elif ordem == "MaiorPreco":
        produtos = produtos.order_by("-preco")
    elif ordem == "MaisVendidos":
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.total_vendas(), produto))
        lista_produtos = sorted(lista_produtos, reverse=True, key=lambda tupla: tupla[0])
        produtos = [item[1] for item in lista_produtos]
    else:
        return produtos
    return produtos