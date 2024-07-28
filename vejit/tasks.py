from crewai import Task
from agents import question_checker, answer_generator, frag, crag


question_checking_task = Task(
    description='''Check if the question {query} is valid based on work ethics and related topics.
                    The criteria for a valid question are:
                    1. The question should be relevant to the automobiles.
                    2. The question should not contain any offensive language.
                    3. The question should not be a personal attack.
    ''',
    expected_output='Valid or Invalid',
    agent=question_checker,
    output_file = 'validity.txt',
)

answer_generation_task = Task(
    description='''Generate an answer on {query} using a custom-trained model based on {vehicle} and provide a confidence score. 
    The answer should be a detailed paragraph for explanation and in bullet points when you have to explain a process or give a step by step guide. 
    And just stop the execution''',
    expected_output='Answer and Confidence Score',
    agent=answer_generator,
    output_file='answer.txt',
)

frag_task = Task(
    description='''Use RAG to fetch answers from documents if the model\'s confidence is low.
    If your confidecnce score is less than 90%, you can use Crag to fetch answers from the web.
    And if your confidence score is more then 90% then print the answer and stop the execution.''',
    expected_output='Answer and Confidence Score',
    agent=frag,
    output_file = 'frag_answer.txt',
)

crag_task = Task(
    description='Search the internet for answers if Frag fails, including a disclaimer about potential inaccuracies.',
    expected_output='Answer with Disclaimer',
    agent=crag,
    output_file = 'crag_answer.txt',
)
