import requests
from crewai.tools import tool

@tool("WikipediaTool")
def wikipedia_tool(query: str) -> str:
    """Busca informações na Wikipedia sobre um tema."""
    url = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exlimit": 1,
        "explaintext": 1,
        "titles": query,
        "format": "json",
        "utf8": 1,
        "redirects": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        return page.get("extract", "Nenhuma informação encontrada.")
