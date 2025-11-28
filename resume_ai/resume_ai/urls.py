from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views # Views padrão de Login/Logout
from core import views as core_views # Importa todas as views do seu app 'core'
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Rotas de Administração
    path('admin/', admin.site.urls),

    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user = True), name='login'),
    path('cadastro/', core_views.CadastroView.as_view(), name='cadastro'),

    # Rota do Logout 
    path('logout/', core_views.logout_page_view, name='logout'),

    # Rota para o Index
    path('', core_views.index, name='index'), 

    # Rota que usa a view com a lógica do Gemini para GET e POST
    path('resumir/', core_views.resumir_pdf_view, name='resumir_pdf'), 

    # Rota das Configurações do Perfil
    path('configuracoes/', core_views.configuracoes_conta_view, name='configuracoes_conta'),

    # Rota do Histórico de PDFs
    path('historico/', core_views.historico_resumos, name='historico'),

    # Rota para Deleção do PDF
    path("historico/deletar/<int:id>/", core_views.deletar_pdf, name="deletar_pdf"),

    # Rota para Alteração de Dados do Usuário
    path('alterar-dados/', core_views.alterar_dados_view, name='alterar_dados'),

    # Rota para Alteração de Senha
    path("alterar-senha/", core_views.alterar_senha, name="alterar_senha"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)