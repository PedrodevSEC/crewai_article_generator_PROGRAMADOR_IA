
# Definição da Crew 
# Este arquivo define a equipe de agentes da CrewAI.
# Cada agente tem um papel ("researcher", "fact_checker", "writer") e executa tarefas específicas ("research_task", "fact_check_task" e "writing_task").

from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task,  before_kickoff, after_kickoff
from src.crewai_article_generator.tools.wikipedia_tool import WikipediaTool
from src.crewai_article_generator.models import ArticleOut
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

# Inicializa o modelo LLM utilizado no projeto (Gemini)
# As variáveis como modelo do LLM (MODEL) e chave secreta da API (GOOGLE_API_KEY) são carregadas do ambiente (.env)
llm = LLM(
    model=os.getenv("MODEL"),
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

@CrewBase
class ArticleGeneratorCrew():
    """
    Classe principal da Crew responsável por orquestrar
    a geração dos artigos. Carrega os agentes e tarefas
    definidos nos arquivos de configuração (.yaml).
    """

    # Listas de agentes e de tarefas para facilitar a execução da Crew. 
    # A execução, dessa maneira, segue a ordem de definição dos agentes e tarefas, por isso, é importante ter cuidado no momento da criação.
    agents: List[BaseAgent]
    tasks: List[Task]

    
    # Caminhos dos arquivos YAML com a definição dos agentes e tarefas
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    # Funções de Debug, utilizadas para acompanhar a Crew antes da execução e depois da execução.
    # @before_kickoff
    # def before_kickoff_function(self, inputs):
    #     print(f"Before kickoff function with inputs: {inputs}")
    #     # return inputs 

    # @after_kickoff
    # def after_kickoff_function(self, result):
    #     print(f"After kickoff function with result: {result}")
    #     # return result

     # =============== AGENTES ===============
    @agent
    def researcher(self) -> Agent:
        """Agente que pesquisa informações sobre o tema usando a Wikipedia."""
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            llm=llm,
            tools=[WikipediaTool()]
        )
    
    @agent
    def fact_checker(self) -> Agent:
        """Agente responsável por validar as informações coletadas."""
        return Agent(
            config=self.agents_config['fact_checker'],
            verbose=True,
            llm=llm,
            tools=[WikipediaTool()]
        )

    @agent
    def writer(self) -> Agent:
        """Agente redator que transforma o relatório validado em artigo completo."""
        return Agent(
            config=self.agents_config['writer'],
            verbose=True,
            llm=llm
        )

    # =============== TAREFAS ===============
    @task
    def research_task(self) -> Task:
        """Tarefa inicial: Coleta de informações sobre o tema."""
        return Task(
            config=self.tasks_config['research_task'],
        )
    
    @task
    def fact_check_task(self) -> Task:
        """Segunda tarefa: Verificação dos dados pesquisados."""
        return Task(
            config=self.tasks_config['fact_check_task']
        )

    @task
    def writing_task(self) -> Task:
        """Tarefa final — Redação do artigo com base nos dados validados."""
        return Task(
            config=self.tasks_config['writing_task'],
            output_pydantic=ArticleOut
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Monta a Crew final com os agentes e tarefas em sequência.
        O processo é sequencial (researcher (research_task) → fact_checker (fact_check_task) → writer (writing_task)).
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_pydantic=ArticleOut,
            max_concurrency=1
        )
