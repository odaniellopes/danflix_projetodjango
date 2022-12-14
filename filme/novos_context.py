#vamos vriar variaveis personalizadas que vai além do que o django já entrega
from .models import Filme

def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]  #ordenando tooodos os filmes em ordem de data_criacao que está la em models // OBS: o "-" na frente significa ordenar ao contrario
    return {"lista_filmes_recentes": lista_filmes} #retorna um dicionario que tem como chave "lista_filmes_recentes e devolve uma variavel a ser utilizada no htm

def lista_filmes_popular(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:8]
    return {"lista_filmes_popular": lista_filmes}

def filme_destaque(request):
    filme = Filme.objects.all()
    if filme:
        filme = Filme.objects.order_by('-data_criacao')[0]
    else:
        filme = None
    return {"filme_destaque": filme}
