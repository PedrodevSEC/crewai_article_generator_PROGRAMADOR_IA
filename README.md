## Article Generator (CrewAI + Wikipedia)

Este repositório foi desenvolvido para o Desafio Programador IA.
O objetivo é criar um sistema gerador de artigos automatizado utilizando um sistema multiagente com o framework CrewAI, tendo como única e exclusiva fonte de informação a Wikipedia.

### 🚀 Objetivo

- Implementar um pipeline de agentes inteligentes capazes de:

  - Pesquisar informações de forma controlada (via API da Wikipedia);
  
  - Validar os dados coletados;
  
  - Gerar um artigo aleatório sobre o tema pesquisado. 

### 🧰 Tecnologias Utilizadas

- Python 3.12.0

- CrewAI (gestão de múltiplos agentes)

- Flask (exposição via API)

- Wikipedia API (ferramenta única de pesquisa)

- Crewai, Pydantic, requests, Flask, Jinja2, etc.

### ⚙️ Pré-requisitos

- Python instalado (3.10≤ versão <3.14)

- Git instalado

- Acesso à internet para consultas na Wikipedia


### 🧩 Instalação e Execução

- 1 - Clonar o repositório
    - git clone https://github.com/PedrodevSEC/crewai_article_generator_PROGRAMADOR_IA.git
    - Navegar até a pasta do projeto
- 2 - Criar e ativar o ambiente virtual

  - **No Windows**
  python -m venv venv
  venv\Scripts\activate
  
  - **No Linux/Mac**
  python3 -m venv venv
  source venv/bin/activate
 - 3 - Instalar as dependências

   - pip install -r requirements.txt
 - 4 - Configuração do arquivo .env
     - Crie um arquivo chamado **.env** na raiz do projeto e adicione as seguintes variáveis de ambiente:
       - **MODEL** → Define o modelo de LLM a ser utilizado.
           - Exemplo: MODEL="google/gemini-2.0-flash"
        - **Chave da API do LLM** → O nome da variável depende do provedor escolhido.
          - Exemplo para o modelo Gemini: "GOOGLE_API_KEY="sua_chave_api".
 - 5 - Executar a aplicação Flask
    - Na raíz do projeto executar: **python run.py**
  
  Com isso, a API estará rodando no seu local: http://localhost:8000.
## 📁 Estrutura do Projeto
  - <img width="286" height="442" alt="image" src="https://github.com/user-attachments/assets/0a156224-5cf3-4a83-a1bf-18020740600d" />

## 🧪 Testes
- **Opção 1: Acesso direto via navegador**

  - Acesse o endereço gerado ao executar a aplicação diretamente no navegador para abrir a interface web do gerador de artigos.
  - Nela, você pode inserir um tópico e visualizar o artigo gerado.

- **Opção 2: Testes via Postman, Insomnia ou similar**
  - Se preferir testar manualmente basta fazer uma requisição POST para essa rota: http://localhost:8000/api/generate, com um corpo JSON da seguinte maneira:
  
     ```json
      {
        "topic": "Inteligência Artificial"
      }
    ```
     - “Inteligência Artificial” é apenas um exemplo, você pode testar qualquer outro termo disponível na Wikipedia.
## 🧾 Resultados

- Abaixo está um exemplo resumido da saída gerada pela API após uma requisição bem-sucedida:

    - Exemplo de Entrada:
    ```json
    {
      "topic": "Inteligência Artificial"
    }
    ```
    - Exemplo de Saída:
      ```json
        {
      "title": "Inteligência Artificial: Uma Visão Abrangente",
      "topic": "Inteligência Artificial",
      "summary": "A Inteligência Artificial (IA) busca simular o pensamento humano em máquinas, abrangendo desde sistemas especialistas até ferramentas generativas. Sua evolução histórica e impacto multidisciplinar são vastos.",
      "word_count": 472,
      "sections": [
        {
          "title": "Visão Geral da Inteligência Artificial",
          "content": "No campo da informática, a Inteligência Artificial (IA) manifesta-se como..."
        },
        {
          "title": "Contexto Histórico da IA",
          "content": "A ideia de inteligência artificial não é recente; Aristóteles já vislumbrava..."
        },
        {
          "title": "Relevância e Impacto da IA",
          "content": "A IA demonstra sua relevância através de aplicações em setores diversificados..."
        }
      ],
      "sources": [
        "https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial"
      ]
    }
      ```
    - Exemplo de Saída (Visual):
      - PDF da página Web com um artigo já gerado: [Gerador de Artigos - CrewAI.pdf](https://github.com/user-attachments/files/23225470/Gerador.de.Artigos.-.CrewAI.pdf)

