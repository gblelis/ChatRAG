import os
from dotenv import find_dotenv, load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Optional

_ = load_dotenv(find_dotenv())

class LLMFactory:
    """Class that includes LLM and Embedding models."""

    def __init__(self, llm_model_name: Optional[str] = None, llm_temperature: Optional[int] = 0.3, embedding_model_name: Optional[str] = None) -> None:

        self.llm = ChatGroq(
            model_name=llm_model_name or 'openai/gpt-oss-20b',
            temperature=llm_temperature,
            api_key=os.getenv('GROQ_API_KEY')
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name or 'BAAI/bge-m3'
        )
    
    def get_llm(self) -> ChatGroq:
        return self.llm
    
    def get_embeddings(self) -> HuggingFaceEmbeddings:
        return self.embeddings