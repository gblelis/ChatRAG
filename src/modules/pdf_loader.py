import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Optional

class PDFProcessor:
    """Read a PDF document and split into chunks."""

    def __init__(self, chunk_size: Optional[int] = 1000, chunk_overlap: Optional[int] = 200) -> None:

        # Initializing Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size or 1000,
            chunk_overlap=chunk_overlap or 200
        )

    def process_pdf(self, uploaded_file: UploadedFile) -> list[Document]:
        """Receives a file from st.file_uploader(), saves temporarily and divides into chunks. Finally, deletes the temporary file.

        Args:
            uploaded_file (UploadedFile): File uploaded by user via Streamlit.

        Returns:
            list[Document]: The text of the PDF divided into chunks (Langchain Documents).
        """

        if uploaded_file is None:
            return []

        # Creates a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        try:
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            return chunks
        finally:
            # Always remove the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)