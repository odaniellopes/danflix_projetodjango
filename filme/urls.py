#url - view - template
from django.urls import path, reverse_lazy
from .views import Homepage, Homefilmes, DetalhesFilme, Pesquisafilme, Paginaperfil, Criarconta
from django.contrib.auth import views as auth_view   #mudei o nome para não confundir com o arquivo que criamos

app_name='filme'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', DetalhesFilme.as_view(), name='detalhesfilme'), #pk é a primary key do banco de dados do modelo que passei logo adiante "Detalhesfilme"
    path('pesquisa/', Pesquisafilme.as_view(), name='pesquisafilme' ),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('editarperfil/<int:pk>', Paginaperfil.as_view(), name='editarperfil'),
    path('criarconta/', Criarconta.as_view(), name='criarconta'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name='editarperfil.html',
                                                             success_url=reverse_lazy('filme:homefilmes')), name='mudarsenha'),
]

