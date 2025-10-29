# Ferramenta personalizada "WikipediaTool"

# Esta classe é usada pelos agentes da Crew para consultar exclusivamente a API da Wikipedia em português.
# Ela busca o título mais relevante e retorna o extrato completo do artigo correspondente.

import requests
from crewai.tools import BaseTool

class WikipediaTool(BaseTool):
    """
    Ferramenta de busca e extração de conteúdo da Wikipedia.
    Utilizada pelos agentes (Researcher (Pesquisador) e Fact Checker (Verificador de fatos)) para
    garantir que todas as informações venham de uma fonte confiável.
    """
    name: str = "Ferramenta de Pesquisa Contextual da Wikipedia"
    description: str = (
        "Útil para pesquisar na API da Wikipedia em português para obter informações abrangentes, relevantes e bem contextualizadas sobre um determinado tema."
    )

    def _run(self, argument: str) -> str:
        """
        Executa a busca na Wikipedia em duas etapas:
        1. Encontra o título mais relevante (usando `list=search`)
        2. Recupera o texto completo da página encontrada (usando `prop=extracts`)
        Retorna o conteúdo puro em texto, sem HTML.
        """

        URL = "https://pt.wikipedia.org/w/api.php"
        headers = {
            "User-Agent": "WikipediaTool/1.0 (CrewarticleGenerator)"
        }
        
        # ETAPA 1: Encontrar o Título Correto usando list=search (Necessário pois as vezes o usuário pode digitar algo errado na entrada da API,
        # ou o título original é um pouco diferente do pesquisado (Ex: "1 guerra mundial", que na verdade o correto é "Primeira Guerra Mundial").)
        search_params = {
            'action': 'query',
            'list': 'search',     # Usar a função de busca
            'srsearch': argument, # Termo pesquisado pelo usuário na API (Ex: microalgas, filosofia, etc...)
            'srlimit': '1',       
            'format': 'json',
            'utf8': '1'
        }
        
        # Tratamento de erros/execeções
        try:
            # Utilização da requests para fazer a pesquisa através de um GET.
            response = requests.get(URL, params=search_params, headers=headers)
            response.raise_for_status()
            # Recupera o dado recebido da Wikipedia
            search_data = response.json()
            
            # Verifica se há resultados válidos
            search_results = search_data.get('query', {}).get('search', [])
            if not search_results:
                return f"Falha na pesquisa: O tópico '{argument}' não foi encontrado na Wikipedia."

            # O título mais relevante encontrado
            found_title = search_results[0]['title'] 
            
            # ETAPA 2: Obtenção do conteúdo completo usando prop=extracts
            extract_params = {
                'action': 'query',
                'prop': 'extracts',
                'exlimit': '1',
                'explaintext': '1',
                'titles': found_title,  # Usar o título exato encontrado na Etapa 1
                'format': 'json',
                'utf8': '1',
                'redirects': '1'
            }
            
            # Utilização da requests para fazer a pesquisa através de um GET.
            response = requests.get(URL, params=extract_params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Processa a Resposta
            pages = data['query']['pages']
            page_id = next(iter(pages))
            page_data = pages[page_id]

            if 'extract' in page_data:
                extract = page_data['extract']
                
                # O ID -1 indica que, mesmo após a busca, não há página
                if page_id == "-1":
                     return f"Falha na pesquisa: O tópico '{argument}' não foi encontrado na Wikipedia."

                # Retorna o texto completo para o Agente Pesquisador
                return extract
            else:
                return f"Falha na pesquisa: Não foi possível encontrar extrato para o tópico '{argument}'."

        except requests.exceptions.RequestException as e:
            return f"Erro ao conectar à API da Wikipedia: {e}"
        except Exception as e:
            return f"Ocorreu um erro inesperado: {e}"