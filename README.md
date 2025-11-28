# Resumidor de PDF com Inteligência Artificial

## 📌 Visão Geral
O **Resumidor de PDF com IA** é uma aplicação web desenvolvida para facilitar a análise e interpretação de documentos extensos em PDF. Utilizando técnicas avançadas de Inteligência Artificial(Gemini), o sistema extrai o conteúdo textual do arquivo e gera automaticamente um resumo claro, objetivo e estruturado.

O projeto foi desenvolvido com foco em **usabilidade**, **eficiência** e **escalabilidade**, possibilitando que empresas e profissionais otimizem tempo em atividades de leitura, revisão e documentação.

---

## 🎯 Principais Funcionalidades
- **Upload de PDF:** O usuário pode fazer o upload de qualquer arquivo PDF diretamente pela interface.
- **Extração Inteligente de Texto:** O sistema identifica, trata e extrai texto mesmo de PDFs complexos.
- **Resumo Gerado por IA:** O conteúdo é processado por um modelo de linguagem natural, gerando resumos coesos e de fácil compreensão.
- **Histórico de PDFs:** Todos os PDFs que o usuário realizou Upload, ficará no Histórico de PDFs.
- **Interface Intuitiva:** Navegação simplificada, com foco em experiência do usuário.

---

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python (Framework: Django)
- **IA:** API da Google IA(Gemini) para geração de resumos
- **Manipulação de PDFs:** Bibliotecas para leitura, extração e geração de arquivos PDF
- **Frontend:** HTML, CSS e Bootstrap
- **Banco de Dados:** SQLite

---

## 🧩 Estrutura do Projeto
``` bash
/project
│── resume_ai           # Pasta do Projeto(Core e Resume.AI)
│     │── core          #
│     │── media         #
│     │── pdfs          #
│     │── resume.ai     #
│     │── .env.example  #
│     │── manage.py     #
│
│── requirements.txt    # Dependências do projeto
│── README.md           # Documentação
```

---

## ⚙️ Como Funciona
1. O usuário acessa a tela inicial e faz upload do PDF.
2. O backend processa e extrai o conteúdo do arquivo.
3. A IA interpreta o texto e gera um resumo conforme padrões definidos.
4. O usuário visualiza o resumo e pode optar por baixar o PDF gerado.
5. O sistema salva o registro no histórico, permitindo consultas futuras.

---

## 🚀 Diferenciais do Projeto
- **Automatiza atividades repetitivas**, reduzindo tempo de leitura e análise.
- **Integração completa com IA**, gerando resultados otimizados.
- **Arquitetura modular**, facilitando melhorias e expansão futura.
- **Experiência de usuário fluida**, com navegação organizada e design limpo.
- **Ideal para empresas**, consultorias, escritórios jurídicos, equipes acadêmicas e profissionais que lidam com PDFs diariamente.

---

## 📂 Casos de Uso
- Análise de documentos jurídicos
- Resumos de artigos, TCCs e materiais acadêmicos
- Processamento de relatórios corporativos
- Avaliação rápida de documentos longos em processos internos

---

## 🧪 Testes e Qualidade
O sistema foi projetado com foco em estabilidade e confiabilidade, passando por testes de:
- Funcionalidade do upload e leitura de PDFs
- Precisão da extração de textos
- Coesão e coerência dos resumos gerados
- Consistência da exportação em PDF
- Validação de comportamento do frontend

---

## 🏁 Conclusão
O **Resumidor de PDF com IA** representa uma solução moderna e eficiente para empresas que buscam otimizar processos de leitura e análise documental. Com uma arquitetura robusta, interface intuitiva e alto desempenho, o sistema adiciona valor aos fluxos de trabalho e aumenta a produtividade de equipes.

Para melhorias futuras, estão previstos módulos de classificação automática de documentos, tradução assistida por IA e integração com nuvem corporativa.


