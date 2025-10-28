import sys
from .crew import ArticleGeneratorCrew

def run():
    """ Run the crew """

    inputs = {
        'topic': "Primeira Guerra Mundial"
    }

    ArticleGeneratorCrew().crew().kickoff(inputs=inputs)


# if __name__ == "__main__":
#     run()