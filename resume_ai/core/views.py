import os
import pypdf
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import logout
from dotenv import load_dotenv
from .models import PDFHistory, PasswordResetCode 
from google import genai
from google.genai.errors import APIError
from .forms import CadastroForm, UpdateUserForm, ChangePasswordForm 
from django.core.files.base import ContentFile
from fpdf import FPDF
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
import random

# VIEW DO HISTÓRICO DE RESUMOS
@login_required
def historico_resumos(request):
    historicos = PDFHistory.objects.filter(user=request.user).order_by('-enviado_em')
    return render(request, 'historico.html', {'historicos': historicos})

# DELETA O PDF DO HISTÓRICO
@login_required
def deletar_pdf(request, id):
    pdf = get_object_or_404(PDFHistory, id=id, user=request.user)

    # Exclui o arquivo físico
    if pdf.arquivo and os.path.exists(pdf.arquivo.path):
        os.remove(pdf.arquivo.path)

    pdf.delete()  # Exclui do banco

    return redirect("historico")

# Importações do Gemini (Adicionadas para o resumo)

# from .models import DocumentoPDF # Se for usar modelos, descomente

# --- CONFIGURAÇÃO GLOBAL DO GEMINI (ROBUSTA) ---
# Carrega a chave de API do .env UMA VEZ
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print(">>> Cliente Gemini inicializado com sucesso.")
    except Exception as e:
        # Se houver erro aqui (chave inválida, problema de conexão, etc.), o cliente será None
        print(f">>> ERRO CRÍTICO: Falha ao inicializar o cliente Gemini. Detalhe: {e}")
else:
    print(">>> ERRO DE CONFIGURAÇÃO: GEMINI_API_KEY não foi encontrada no .env.")
# -----------------------------------------------

User = get_user_model()


# --- 1. VIEW DE PÁGINA INICIAL (INDEX) ---
@login_required
def index(request):
    return render(request, 'index.html', {'titulo': 'Página Inicial'})

# --- 2. VIEW DE CONFIGURAÇÕES DE CONTA ---
@login_required
def configuracoes_conta_view(request):
    """Renderiza o painel de configurações para alterar/excluir conta."""
    return render(request, 'configuracoes.html', {'titulo': 'Configurações de Conta'})

# --- VIEW DE ALTERAÇÃO DE DADOS DO USUÁRIO ---
@login_required
def alterar_dados_view(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados alterados com sucesso!")
            return redirect('alterar_dados')
    else:
        form = UpdateUserForm(instance=user)

    return render(request, 'alterar_dados.html', {'form': form})

# --- 3. VIEW DE CADASTRO ---
class CadastroView(CreateView):
    model = User
    form_class = CadastroForm
    template_name = 'cadastro.html'
    success_url = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index') 
        return super().dispatch(request, *args, **kwargs)


# --- 4 VIEW DE LOGOUT ---
def logout_page_view(request):
    logout(request)  
    return render(request, 'logout.html')

# --- 5. VIEW DE RESUMO PDF ---
@login_required
def resumir_pdf_view(request):
    """Lida com GET (renderiza formulário) e POST (processa resumo com Gemini)."""
    
    # Checagem de Disponibilidade da API
    if client is None:
        if request.method == 'POST':
            return JsonResponse({'error': 'O serviço de IA está indisponível. Verifique a chave de API.'}, status=503)
        return render(request, 'resumir_pdf.html')

    if request.method == 'POST':
        # 1. Receber PDF
        uploaded_file = request.FILES.get('pdf_file')
        language = request.POST.get('language', 'Português')

        if not uploaded_file:
            return JsonResponse({'error': 'Nenhum arquivo PDF enviado.'}, status=400)

        # 2. Extrair texto do PDF
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

        except Exception as e:
            return JsonResponse({'error': f'Erro ao processar PDF (pypdf): {e}'}, status=500)

        if not text.strip():
            return JsonResponse({'error': 'O PDF não contém texto legível.'}, status=400)

        # 3. Chamar a API do Gemini
        try:
            prompt = (
                f"Resuma o seguinte texto de um documento PDF. "
                f"O resumo deve ser conciso, com 3 a 5 parágrafos, no idioma **{language}**.\n\n"
                f"{text}"
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            resumo = response.text

            if not resumo:
                return JsonResponse({'error': 'A API retornou uma resposta vazia.'}, status=500)

        except Exception as e:
            return JsonResponse({'error': f'Erro ao gerar resumo: {e}'}, status=500)

        # 4. Criar PDF com o resumo gerado
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for linha in resumo.split("\n"):
            pdf.multi_cell(0, 10, linha)

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        pdf_file = ContentFile(pdf_bytes)

        nome_pdf = f"resumo_{uploaded_file.name.replace('.pdf','')}.pdf"

        # 5. Salvar PDF do resumo no banco
        registro = PDFHistory.objects.create(user=request.user)
        registro.arquivo.save(nome_pdf, pdf_file)

        # 6. Retornar resumo para a tela
        return JsonResponse({'summary': resumo}, status=200)

    # GET
    return render(request, 'resumir_pdf.html')

# --- 6. VIEW DE ALTERAÇÃO DE SENHA ---
@login_required
def alterar_senha(request):
    user = request.user

    # Se clicou em "esqueci minha senha"
    if "esqueci" in request.GET:
        # Gera código
        codigo = str(random.randint(100000, 999999))
        expira = timezone.now() + timezone.timedelta(minutes=10)

        # Atualiza ou cria o código
        reset_obj, created = PasswordResetCode.objects.get_or_create(user=user)
        reset_obj.code = codigo
        reset_obj.expires_at = expira
        reset_obj.save()

        # Envia e-mail
        send_mail(
            "Código de verificação - Alteração de senha",
            f"Seu código de verificação é: {codigo}",
            None,
            [user.email],
        )

        messages.info(request, "Código de verificação enviado para seu e-mail!")
        form = ChangePasswordForm(initial={"modo": "codigo"})
        return render(request, "alterar_senha.html", {"form": form, "modo": "codigo"})

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        modo = request.POST.get("modo")

        if modo == "senha":
            # Valida senha atual
            atual = request.POST.get("campo_verificacao")

            if not user.check_password(atual):
                messages.error(request, "Senha atual incorreta.")
                return render(request, "alterar_senha.html", {"form": form, "modo": "senha"})

            # Troca senha
            user.set_password(request.POST.get("nova_senha"))
            user.save()
            messages.success(request, "Senha alterada com sucesso!")
            return redirect("login")

        else:
            # Verifica código
            codigo_digitado = request.POST.get("campo_verificacao")

            try:
                reset = PasswordResetCode.objects.get(user=user)
            except PasswordResetCode.DoesNotExist:
                messages.error(request, "Nenhum código de verificação encontrado.")
                return redirect("alterar_senha")

            if not reset.is_valid():
                messages.error(request, "Código expirado. Gere outro.")
                reset.delete()
                return redirect("alterar_senha")

            if reset.code != codigo_digitado:
                messages.error(request, "Código incorreto.")
                return render(request, "alterar_senha.html", {"form": form, "modo": "codigo"})

            # OK → troca senha
            user.set_password(request.POST.get("nova_senha"))
            user.save()
            reset.delete()

            messages.success(request, "Senha alterada com sucesso!")
            return redirect("login")

    form = ChangePasswordForm(initial={"modo": "senha"})
    return render(request, "alterar_senha.html", {"form": form, "modo": "senha"})
