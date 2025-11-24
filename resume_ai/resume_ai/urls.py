from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views # Views padrão de Login/Logout
from core import views as core_views # Importa todas as views do seu app 'core'

urlpatterns = [
    # Rotas de Administração
    path('admin/', admin.site.urls),

    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', core_views.CadastroView.as_view(), name='cadastro'),

    # Rotas da Aplicação (App 'core')
    path('', core_views.index, name='index'), 
    # Rota que usa a view com a lógica do Gemini para GET e POST
    path('resumir/', core_views.resumir_pdf_view, name='resumir_pdf'), 
]