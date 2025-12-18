from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from streamlit.runtime.uploaded_file_manager import UploadedFile
from operator import itemgetter

from modules.llm_factory import LLMFactory
from modules.pdf_loader import PDFProcessor
from modules.vector_db import VectorDBManager

class RAGController:
    """Class that orchestrates the entire process of reading PDFs and LLM inference."""

    def __init__(self) -> None:
        self.llm_factory = LLMFactory()
        self.pdf_processor = PDFProcessor()
        self.vector_db = VectorDBManager(self.llm_factory.get_embeddings())

        self.rag_chain = None

    def ingest_pdfs(self, uploaded_files: list[UploadedFile]) -> tuple[str, bool]:
        """Read the PDF file sent by user, divides into chunks, index all chunks into a Vector Store and configures the LLM chain.

        Args:
            uploaded_files (UploadedFile): List of files uploaded by user via Streamlit.

        Returns:
            bool: Returns True if there are any chunks, False if there aren't.
        """

        all_chunks = []
        files_processed = 0
        files_ignored = []

        for file in uploaded_files:
            try:
                chunks = self.pdf_processor.process_pdf(file)
                if chunks:
                    all_chunks.extend(chunks)
                    files_processed += 1
            except ValueError:
                files_ignored.append(f'{file.name} (Not readable PDF file.)')
            except Exception as e:
                files_ignored.append(f'{file.name} (Error processing PDF file.)')

            if not all_chunks:
                return ('No valid PDF was uploaded. Your files may be not readable or corrupted.', False)

            self.vector_db.add_documents(all_chunks)
            if self.rag_chain is None:
                self._setup_conversational_chain()

            status_text = f'Success! {files_processed} indexed PDFs.'
            if files_ignored:
                status_text += f'\n\nIgnored files:\n' + '\n- '.join(files_ignored)
            
            return (status_text, True)

    def clear_memory(self) -> None:
        """Clears the vector store and the created chain."""

        self.vector_db.clear()
        self.rag_chain = None

    def _setup_conversational_chain(self) -> None:
        """Configures RAG Chain using LCEL. Retriever -> Formatting -> Prompt -> LLM -> String"""

        llm = self.llm_factory.get_llm()
        retriever = self.vector_db.get_retriever()

        # 1. Prompt
        system_prompt = """
        Você é um assistente virtual num ChatBot, responda no idioma da pergunta enviada.
        Serão passados arquivos em PDF pelo usuário e será utilizado RAG como contexto.
        Use o contexto para responder às perguntas.
        Se não souber a resposta, diga educadamente que essa informação não consta nos documentos enviados.
        Você terá acesso ao histórico de conversa para entender melhor o contexto de perguntas do usuário.
        
        Contexto do Documento:
        {context}
        """
        prompt = ChatPromptTemplate.from_messages([
            ('system', system_prompt),
            MessagesPlaceholder(variable_name='chat_history'),
            ('human', '{input}')
        ])

        # 2. Join chunk contents
        def format_docs(docs):
            return '\n\n'.join(doc.page_content for doc in docs)

        # 3. Chain
        self.rag_chain = (
            {
                'context': itemgetter('input') | retriever | format_docs,
                'chat_history': itemgetter('chat_history'),
                'input': itemgetter('input')
            }
            | prompt
            | llm
            | StrOutputParser()
        )

    def get_answer(self, query: str, chat_history: list) -> str:
        if not self.rag_chain:
            return 'Please, upload the documents first.'
        
        # The return is already the final string with StrOutputParser
        return self.rag_chain.invoke({
            'input': query,
            'chat_history': chat_history
        })

    def get_vector_stats(self) -> dict:
        return self.vector_db.get_stats()