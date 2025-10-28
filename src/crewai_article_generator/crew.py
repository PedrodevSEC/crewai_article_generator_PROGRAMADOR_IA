from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task,  before_kickoff, after_kickoff
from src.crewai_article_generator.tools.wikipedia_tool import WikipediaTool
from src.crewai_article_generator.models import ArticleOut
# from src.crewai_article_generator.tools.pdf_generator_tool import PDFGeneratorTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os


# Define o modelo Gemini via CrewAI
llm = LLM(
    model=os.getenv("MODEL"),
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

@CrewBase
class ArticleGeneratorCrew():
    "ArticleGenerator Crew"

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    print(agents_config)
    
    # @before_kickoff
    # def before_kickoff_function(self, inputs):
    #     print(f"Before kickoff function with inputs: {inputs}")
    #     # return inputs 

    # @after_kickoff
    # def after_kickoff_function(self, result):
    #     print(f"After kickoff function with result: {result}")
    #     # return result

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            llm=llm,
            tools=[WikipediaTool()]
        )
    
    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker'],
            verbose=True,
            llm=llm,
            tools=[WikipediaTool()]
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True,
            llm=llm
        )
    
    # @agent
    # def formatter(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['formatter'],
    #         verbose=True,
    #         llm=llm
    #     )
    
    # @agent
    # def reporter(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['reporter'],
    #         verbose=True,
    #         llm=llm,
    #         tools=[PDFGeneratorTool()]
    #     )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )
    
    @task
    def fact_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['fact_check_task']
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
            output_pydantic=ArticleOut
        )
    
    # @task
    # def format_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['format_task']
    #     )

    # @task
    # def generate_pdf_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['generate_pdf_task']
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the ArticleGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
