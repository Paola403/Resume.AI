import os
import pypdf
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from dotenv import load_dotenv

# Importações do Gemini (Adicionadas para o resumo)
from google import genai
from google.genai.errors import APIError

from .forms import CadastroForm 
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


# --- 2. VIEW DE CADASTRO ---
# Mantém a sua lógica de CadastroView
class CadastroView(CreateView):
    model = User
    form_class = CadastroForm
    template_name = 'cadastro.html'
    success_url = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index') 
        return super().dispatch(request, *args, **kwargs)


# --- 3. VIEW DE RESUMO PDF (CRUCIAL PARA A IA) ---
@login_required
def resumir_pdf_view(request):
    """Lida com GET (renderiza formulário) e POST (processa resumo com Gemini)."""
    
    # Checagem de Disponibilidade da API
    if client is None:
        if request.method == 'POST':
            return JsonResponse({'error': 'O serviço de IA está indisponível. Verifique a chave de API no .env.'}, status=503)
        return render(request, 'resumir_pdf.html') 


    if request.method == 'POST':
        # 1. Recebe dados e arquivo
        uploaded_file = request.FILES.get('pdf_file')
        language = request.POST.get('language', 'Português') 

        if not uploaded_file:
            return JsonResponse({'error': 'Nenhum arquivo PDF enviado.'}, status=400)
            
        # 2. Extrair o texto do PDF
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        except Exception as e:
            return JsonResponse({'error': f'Erro ao processar PDF (pypdf): {e}'}, status=500)
        
        if not text.strip():
             return JsonResponse({'error': 'O PDF não contém texto legível ou está vazio.'}, status=400)

        # 3. Chamar a API do Gemini
        try:
            prompt = (
                f"Resuma o seguinte texto de um documento PDF. O resumo deve ser conciso, ter de 3 a 5 parágrafos e estar no idioma **{language}**.\n\n"
                f"TEXTO DO PDF:\n{text}"
            )

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            if not response.text:
                 return JsonResponse({'error': 'A API bloqueou a resposta ou retornou vazia.'}, status=500)
            
            return JsonResponse({'summary': response.text}, status=200)

        except APIError as e:
            return JsonResponse({'error': f'Erro específico da API Gemini (Chave/Cota): {e}'}, status=500)
        
        except Exception as e:
            return JsonResponse({'error': f'Erro inesperado na chamada da API: {e}'}, status=500)

    # Se a requisição for GET, renderiza a página do formulário
    return render(request, 'resumir_pdf.html')