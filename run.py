# Script principal do sistema (ponto de entrada da API)

# Este arquivo apenas inicializa a aplicação Flask e executa o servidor local na porta 8000.
# A função create_app() é importada do módulo src.app, onde as rotas e Blueprints são configurados.

from src.app import create_app

# Cria a instância principal do aplicativo
app = create_app()

if __name__ == "__main__":
    # Executa o servidor na rede local e ativa o modo debug (facilita o teste dos agentes e da API)
    app.run(host="0.0.0.0", port=8000, debug=True)

