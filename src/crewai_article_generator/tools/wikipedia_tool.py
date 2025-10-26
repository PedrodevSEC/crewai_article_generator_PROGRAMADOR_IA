import requests
import json
from crewai.tools import BaseTool

class WikipediaTool(BaseTool):
    # 1. Definição da Ferramenta
    name: str = "Ferramenta de Pesquisa Contextual da Wikipedia"
    description: str = (
        "Útil para pesquisar na API da Wikipedia em português para obter informações abrangentes, relevantes e bem contextualizadas sobre um determinado tema."
    )

    def _run(self, argument: str) -> str:
        """
        Consulta a API da Wikipedia para obter um extrato sobre o tópico.
        O tópico a ser pesquisado será fornecido pelo Agente Pesquisador.
        """
        
        # 2. Configuração da API
        # A URL base e os parâmetros são baseados no exemplo fornecido no projeto 
        URL = "https://pt.wikipedia.org/w/api.php"
        
        # Parâmetros otimizados para obter o extrato de texto
        params = {
            'action': 'query',
            'prop': 'extracts',
            'exlimit': '1',       # Retorna apenas 1 resultado
            'explaintext': '1',   # Retorna o texto simples (sem HTML/Wiki markup)
            'titles': argument,      # O tópico que o Agente está pesquisando
            'format': 'json',
            'utf8': '1',
            'redirects': '1'
        }
        
        # 3. Realiza a Requisição
        try:    
            headers = {
                "User-Agent": "WikipediaTool/1.0 (CrewarticleGenerator)"
            }
            response = requests.get(URL, params=params, headers=headers)
            response.raise_for_status() # Lança uma exceção para erros HTTP
            data = response.json()

            # 4. Processa a Resposta (Extração do Conteúdo)
            pages = data['query']['pages']
            
            # O ID da página é a chave que muda.
            # Basta pegar o primeiro (e único (a wikipedia sempre retornar apenas um único resultado para um título específico)) ID de página na resposta.
            page_id = next(iter(pages))
            page_data = pages[page_id]

            if 'extract' in page_data:
                extract = page_data['extract']
                
                # Se a página for de erro (ex: não encontrada).
                if page_id == "-1" or "página não existe" in extract.lower() or "redireciona" in extract.lower():
                    return f"Falha na pesquisa: O tópico '{argument}' não foi encontrado na Wikipedia."
                
                # Retorna o texto completo para o Agente Pesquisador
                return extract
            else:
                return f"Falha na pesquisa: Não foi possível encontrar extrato para o tópico '{argument}'."

        except requests.exceptions.RequestException as e:
            # Lida com erros de rede ou HTTP
            return f"Erro ao conectar à API da Wikipedia: {e}"
        except Exception as e:
            # Lida com outros erros (ex: erro no processamento do JSON)
            return f"Ocorreu um erro inesperado: {e}"

# Exemplo de uso (Para teste, não inclua no código final do CrewAI, pois o Agente fará isso):
# if __name__ == '__main__':
#     wikipedia_search = WikipediaTool()
#     # O exemplo de URL dado usa 'Futebol' [cite: 15]
#     result = wikipedia_search._run("Futebol brasileiro") 
#     print(result)
