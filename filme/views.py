from django.shortcuts import render, redirect, reverse
from.models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarcontaForm, FormHomepage


# Create your views here.
class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:   #redirecionara para a homefilmes
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)  # redireciona para a homepage

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')



#url - view - template
class Homefilmes(LoginRequiredMixin ,ListView):
    template_name = 'homefilmes.html'
    model = Filme   #modelo do banco de dados
    #a partir daqui ele irá exibir a lista mas como "object_views" cada filme então mude la na homefilmes.html  -> lista de itens do modelo


class DetalhesFilme(LoginRequiredMixin ,DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object -> 1 item do nosso modelo

    #contabiliza visualização
    def get(self, request, *args, **kwargs):   #contabilizando as visualizações
        #descobrir qual filme ele esta assistindo
        filme = self.get_object()
        #somar mais um nas visualizacoes
        filme.visualizacoes += 1
        #salvar
        filme.save()
        #mesclar o usuario com as visualizações
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        #retorna
        return super().get(request, *args, **kwargs) #redireciona o usuario para a url final

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        #filtrar a tabela de filmes para que pegue os filmes de mesma categoria do atual(do object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]  #passando um parametro que limita quantos filmes dessa categoria. no caso são até 5
        context['filmes_relacionados'] = filmes_relacionados
        return context

class Pesquisafilme(LoginRequiredMixin ,ListView):
    template_name = 'pesquisa.html'
    model = Filme
    #object_list     #é assim que ela aparece

#editando e filtrando o nosso object_list(lista dos filmes)
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)    #poderia ser tambem descricao__icontains, episodio__icontains
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarcontaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')  #ele leva o usuário para um LINK! (https//...)









###caso queira utilizar functions ao invés de classes
#def homepage(request):
#    return render(request, 'homepage.html')

#def homefilmes(request):
#    context = {}
#    lista_filmes = Filme.objects.all()   #pegando os filmes do banco de dados
#    context['lista_filmes'] = lista_filmes
#    return render(request, 'homefilmes.html', context)