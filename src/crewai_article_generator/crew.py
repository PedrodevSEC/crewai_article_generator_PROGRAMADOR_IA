from crewai import Agent, Crew, Task, Process, LLM
from tools.wikipedia_tool import wikipedia_tool
import os

# Configura a chave da API do Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyBo3Mv_D6z3mfA5Ob6nbFKDSZkqI9X5k4o"

# Define o modelo Gemini via CrewAI
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)


# Cria o agente pesquisador
researcher = Agent(
    role="Pesquisador de Artigos",
    goal="Pesquisar informações detalhadas sobre qualquer tema solicitado.",
    backstory="Um agente especialista em encontrar e resumir informações relevantes da Wikipedia.",
    tools=[wikipedia_tool],  # sem parênteses!
    llm=llm
)

# Cria a tarefa
research_task = Task(
    description="Pesquisar informações sobre o tema: 'Inteligência Artificial'.",
    expected_output="Um resumo detalhado do tema, com 300 palavras.",
    agent=researcher
)

# Monta a crew (apenas o agente pesquisador por enquanto)
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    # process=Process.sequential
)

# Função para executar
def run_research():
    result = crew.kickoff()
    print(result)
