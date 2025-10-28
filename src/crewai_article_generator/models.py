from pydantic import BaseModel, Field, ValidationError
from typing import List

class Section(BaseModel):
    title: str = Field(..., description="Título da seção do artigo")
    content: str = Field(..., description="Texto da seção correspondente")

class ArticleOut(BaseModel):
    topic: str = Field(..., description="Tema principal do artigo")
    title: str = Field(..., description="Título do artigo")
    summary: str = Field(..., min_length=50, max_length=500, description="Resumo introdutório")
    word_count: int = Field(..., ge=300, description="Número total de palavras")
    sections: List[Section] = Field(..., description="Lista de seções do artigo")
    sources: List[str] = Field(default_factory=list, description="Fontes de referência utilizadas")

def validate_article_json(data: dict) -> ArticleOut:
    """
    Valida o JSON retornado pela CrewAI garantindo que siga o modelo ArticleOut.
    Retorna um objeto ArticleOut se estiver válido, ou lança um erro se não estiver.
    """
    try:
        article = ArticleOut(**data)
        return article
    except ValidationError as e:
        raise ValueError(f"Erro de validação Pydantic: {e}")