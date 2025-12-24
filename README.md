# 🤖 ChatRAG: Converse com seus Documentos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Fast_Inference-orange?style=for-the-badge)

**ChatRAG** é uma aplicação RAG (Retrieval-Augmented Generation) construída com Python. Ela permite que usuários façam upload de múltiplos documentos PDF e conversem com eles utilizando LLMs via **Groq**, mantendo o contexto da conversa.

O projeto é estruturado utilizando princípios de **POO (Programação Orientada a Objetos)** e padrões modernos do **LangChain (LCEL)** para robustez e escalabilidade.

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/c96ad8c8-114b-4589-94c7-320e5a786740" />

---

## ✨ Funcionalidades Principais

* **Suporte Multi-PDF**: Faça upload e indexe vários arquivos PDF simultaneamente.
* **Indexação Incremental**: Adicione novos documentos ao contexto existente sem precisar reprocessar tudo do zero.
* **Chat Contextual**: A IA lembra dos turnos anteriores da conversa (Histórico do Chat) para responder perguntas de acompanhamento com precisão.
* **Inferência Rápida**: Utiliza a API da Groq para respostas quase instantâneas.
* **Busca Vetorial Local**: Utiliza **FAISS** para armazenamento e recuperação eficiente de vetores na CPU.
* **Gerenciamento de Memória**: Controles simples na interface para resetar o contexto e o histórico do chat.

---

## 🛠️ Tecnologias Utilizadas

* **Front-end**: [Streamlit](https://streamlit.io/)
* **Orquestração**: [LangChain](https://langchain.com/) (Core, Community, Groq)
* **Provedor de LLM**: [Groq](https://groq.com/)
* **Banco Vetorial**: [FAISS](https://github.com/facebookresearch/faiss) (Versão CPU)
* **Embeddings**: [HuggingFace](https://huggingface.co/) (`BAAI/bge-m3`)
* **Gerenciador de Pacotes**: [uv](https://github.com/astral-sh/uv) (Recomendado) ou pip

---

## 📂 Estrutura do Projeto

```text
ChatRAG/
├── .env                  # Configuração das Chaves de API
├── .python-version       # Arquivo de versão do Python
├── pyproject.toml        # Dependências (uv)
├── README.md             # Documentação do projeto
├── requirements.txt      # Requisitos de pacotes do python
├── uv.lock               # Arquivo de sincronização do uv (Versionamento de pacotes)
└── src/
    ├── __init__.py
    ├── app.py            # Ponto de entrada (Frontend Streamlit)
    ├── controller.py     # Orquestrador (Lógica RAG & Gerenciamento de Estado)
    └── modules/
        ├── __init__.py
        ├── llm_factory.py    # Fábrica para modelos de LLM e Embeddings
        ├── pdf_loader.py     # Lógica de processamento e chunking de PDF
        └── vector_db.py      # Gerenciamento do FAISS Vector Store
```

---

## 🚀 Como Iniciar

### Pré-requisitos:

1. Python 3.10 instalado.

2. Groq API Key: Obtenha uma gratuitamente em [console.groq.com](console.groq.com).

3. (Opcional) `uv` instalado para gerenciamento rápido de dependências.

### Instalação:

1. Clone o repositório:

```bash
git clone https://github.com/gblelis/ChatRAG.git
cd ChatRAG
```

2. Instale as Dependências:

- Usando `uv` (Recomendado):

```bash
uv sync
```

- Usando `pip` padrão:

```bash
pip install -r requirements.txt
```

3. Configure o Ambiente: Crie um arquivo `.env` na raiz do projeto:

```bash
GROQ_API_KEY=gsk_sua_chave_aqui
```

## ▶️ Como Usar

Rode a aplicação usando o Streamlit:

```bash
# Usando uv
uv run streamlit run src/app.py

# Ou usando python padrão
streamlit run src/app.py
```

O app abrirá no seu navegador em `http://localhost:8501`.

1. **Upload**: Use a barra lateral para carregar um ou múltiplos arquivos PDF.

2. **Adicionar** ao Contexto: Clique em "Add PDFs to context" para indexar o conteúdo.

3. **Chat**: Digite suas perguntas no campo principal. A IA responderá baseada apenas nos documentos fornecidos.

4. **Limpar**: Use o botão de lixeira na barra lateral para limpar a memória e começar do zero.

---

## 🧠 Visão da Arquitetura

O projeto segue um padrão limpo de Controller-Service:

- `app.py`: Lida com a renderização da UI e gerenciamento do Estado da Sessão (`st.session_state`). Delega toda a lógica para o Controller.

- `controller.py`: O cérebro da operação. Inicializa os módulos e constrói o pipeline LangChain LCEL:

    - Input -> Retriever + Histórico -> Prompt -> LLM -> Output.

- `vector_db.py`: Gerencia o FAISS. Suporta `create_from_documents` (sobrescrever) e `add_documents` (atualização incremental).

- `pdf_loader.py`: Lida com arquivos temporários, carregamento via `PyPDFLoader` e divisão de texto usando `RecursiveCharacterTextSplitter`.

---

## 📝 Licença

MIT License © 2025 Gabriel Lelis