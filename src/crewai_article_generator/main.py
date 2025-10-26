import sys
from crew import ArticleGerneratorCrew

def run():
    """ Run the crew """

    inputs = {
        'topic': "Brasil"
    }

    ArticleGerneratorCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
