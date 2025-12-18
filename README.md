# 🤖 ChatRAG: Converse com seus Documentos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=LangChain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Fast_Inference-orange?style=for-the-badge)

**ChatRAG** é uma aplicação RAG (Retrieval-Augmented Generation) "Simples & Rápida" construída com Python. Ela permite que usuários façam upload de múltiplos documentos PDF e conversem com eles utilizando LLMs de última geração via **Groq** (Llama 3, Mixtral, etc.), mantendo o contexto da conversa.

O projeto é estruturado utilizando princípios de **POO (Programação Orientada a Objetos)** e padrões modernos do **LangChain (LCEL)** para robustez e escalabilidade.

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
* **Embeddings**: [HuggingFace](https://huggingface.co/) (`BAAI/bge-m3` ou similar)
* **Gerenciador de Pacotes**: [uv](https://github.com/astral-sh/uv) (Recomendado) ou pip

---

## 📂 Estrutura do Projeto

```text
ChatRAG/
├── .env                  # Configuração das Chaves de API
├── .python-version       # Arquivo de versão do Python
├── pyproject.toml        # Dependências (uv)
├── README.md             # Documentação do projeto
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