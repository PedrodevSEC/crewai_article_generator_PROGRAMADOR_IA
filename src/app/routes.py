# Rotas da API Flask (interface entre aplicação e CrewAI)

# Define os endpoints REST:
# - "/" renderiza a página HTML principal.
# - "/api/generate" executa a Crew e retorna o JSON do artigo.


from flask import Blueprint, render_template, request, jsonify
from src.crewai_article_generator.crew import ArticleGeneratorCrew
from src.crewai_article_generator.models import ArticleOut

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    """
    Rota /"home", apenas uma maneira visual de testar o sistema.
    """
    return render_template("index.html")

@bp.route("/api/generate", methods=["POST"])
def generate_article():
    """
    Rota principal que recebe um 'topic' (tema) e executa a CrewAI para gerar o artigo.
    - Recebe o JSON com o campo 'topic'
    - Chama o pipeline da Crew (ArticleGeneratorCrew)
    - Retorna o artigo validado no formato JSON
    """
    data = request.get_json(force=True)
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Campo 'topic' é obrigatório."}), 400

    # Executa a crew passando o tópico como entrada
    result = ArticleGeneratorCrew().crew().kickoff(inputs={"topic": topic})

    # Assume que a saída é um modelo Pydantic (ArticleOut)
    if hasattr(result, "pydantic") and result.pydantic:
        article: ArticleOut = result.pydantic
        return jsonify(article.model_dump()), 200

    # Caso a crew não retorne o esperado (situação excepcional)
    return jsonify({
        "error": "Falha ao processar a saída da CrewAI.",
        "debug": str(result)[:300]
    }), 500