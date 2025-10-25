from flask import Blueprint, request, jsonify
from .services.crew_manager import generate_article

routes = Blueprint("routes", __name__)

@routes.route("/generate", methods=["GET"])
def generate():
    topic = request.args.get("topic")
    if not topic:
        return jsonify({"error": "Parâmetro 'topic' é obrigatório"}), 400

    try:
        article = generate_article(topic)
        return jsonify(article)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
