# Definição do modelo de dados com Pydantic

# Este modelo garante que o JSON retornado pela CrewAI siga um formato padronizado e validado antes de ser enviado pela API. 

from pydantic import BaseModel, Field, ValidationError
from typing import List

class Section(BaseModel):
    """Representa uma seção individual do artigo."""
    title: str = Field(..., description="Título da seção do artigo")
    content: str = Field(..., description="Texto da seção correspondente")

class ArticleOut(BaseModel):
    """
    Estrutura de saída final do artigo gerado pela CrewAI.
    """
    topic: str = Field(..., description="Tema principal do artigo")
    title: str = Field(..., description="Título do artigo")
    summary: str = Field(..., min_length=50, max_length=500, description="Resumo introdutório")
    word_count: int = Field(..., ge=300, description="Número total de palavras")
    sections: List[Section] = Field(..., description="Lista de seções do artigo")
    sources: List[str] = Field(default_factory=list, description="Fontes de referência utilizadas")

