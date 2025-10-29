# Script que cria a API (App Flask)
from flask import Flask

def create_app():
    # Configuração do app, com as pastas templates e static
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Importa a Blueprint das rotas e registra no app
    from .routes import bp
    app.register_blueprint(bp)

    return app