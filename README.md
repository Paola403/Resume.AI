# 📄 Resume.AI — Sistema de Resumo de PDFs com Histórico e Autenticação

O **Resume.AI** é um sistema web desenvolvido em **Django** com foco em produtividade, permitindo que usuários façam upload de arquivos PDF e recebam um resumo automático gerado por IA.  
Além disso, o sistema conta com funcionalidades de autenticação completa, histórico de arquivos resumidos e gerenciamento de perfil.

---

## 🚀 Tecnologias Utilizadas

- **Python 3**
- **Django**
- **HTML + CSS + JavaScript**
- **OpenAI API (para resumo)**
- **SQLite / MySQL**
- **dotenv**
- **pypdf**

---

## 🧩 Funcionalidades Principais

### 🔐 Autenticação
- Cadastro de usuário  
- Login  
- Logout  
- Alterar dados do perfil  
- Alterar senha com verificação  

- Fluxo completo de *Esqueci minha senha* com:
  - Código de verificação de 6 dígitos  
  - Expiração automática  
  - Validação antes da troca da senha
- OBS(Fluxo de Esqueci minha senha Incompleto)

### 📄 Resumo de PDF
- Upload de arquivos PDF  
- Extração automática do texto  
- Envio para IA gerar resumo  
- Exibição na interface  
- Salvamento automático no histórico  

### 📁 Histórico
- Lista de PDFs resumidos  
  - Resumo gerado  

---

## 🧪 Testes Automatizados

O projeto inclui testes cobrindo:

- Registro  
- Login e logout  
- Alteração de dados  
- Alteração de senha  
- Fluxo de esqueci minha senha  

---

## 📂 Como Rodar Localmente o Projeto

No ambiente Linux:

```console
git clone https://github.com/Paola403/Resume.AI.git
cd resume_ai/
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd resume_ai/
python manage.py migrate
python manage.py test
coverage run --source='.' manage.py test 
coverage html
python manage.py runserver
```

No ambiente Windows:

```console
git clone https://github.com/Paola403/Resume.AI.git
cd resume_ai/
pip install virtualenv venv
cd venv
cd scripts
activate.bat
cd ..
cd ..
pip install -r requirements.txt
cd resume_ai/
python manage.py migrate
python manage.py test
coverage run --source='.' manage.py test 
coverage html
python manage.py runserver

```
---

## ⚙️ Colocando a chave da API

- Renomeie o .env.example para apenas **.env**
- Coloque a cheve da API do Google AI (Gemini)

---

## 📌 Diferenciais

- Fluxo seguro de recuperação de senha

- Histórico completo de arquivos processados

- Interface simples e intuitiva

- Integração com inteligência artificial

- Código organizado e fácil de manter

---

## 🔧 Melhorias Futuras

- Melhorar layout final das telas
- Tema escuro
- Exportar resumo para PDF
- Gestão de favoritos

---

## 🏗️ Status do Projeto
_Este projeto ainda está em desenvolvimento e NÃO está 100% finalizado._


