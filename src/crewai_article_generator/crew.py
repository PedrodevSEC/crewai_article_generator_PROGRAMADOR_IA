from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task,  before_kickoff, after_kickoff
from tools.wikipedia_tool import WikipediaTool
from crewai_tools import SerperDevTool
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
class ArticleGerneratorCrew():
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
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ArticleGenerator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
