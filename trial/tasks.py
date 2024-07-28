from crewai import Task
from agents import tech_support_agent1,tech_support_agent2, customer_agent, writer_agent, json_converter_agent
from tools import pdf_reader_tool
from net_tool import net_tool

# customer_inquiry_task = Task(
#     description='''Generate questions about {topic} in the first person perspective, simulating how a customer might ask them.
#     For example, if the topic is related to car maintenance, a question might be "My steering wheel is making noise; what should I do?".
#     For each {topic} in the list, generate a sequence of follow-up questions from the customer's perspective.
#     Once you have generated a question, send it to the formatter so that it can format the question into a JSON file.
#     ''',
#     expected_output='A list of first-person questions from the customer.',
#     tools=[net_tool],
#     agent=customer_agent,
# )


# technical_support_task1 = Task(
#     description='Answer the customer’s questions about {topic} using the provided vehicle’s owner manual.',
#     expected_output='Answers to the customer’s questions.',
#     tools=[pdf_reader_tool],
#     agent=tech_support_agent1,
# )

# technical_support_task2 = Task(
#     description='Answer the customer’s questions about {topic} using the provided vehicle’s owner manual.',
#     expected_output='Answers to the customer’s questions.',
#     tools=[pdf_reader_tool],
#     agent=tech_support_agent2,
# )

# writing_task = Task(
#     description='''
#         Combine and refine answers from technical support agents about {topic} into a well-formatted customer care response.
#         Ensure the response is detailed and includes explanations for any tough or technical terms. The response should be at least 100 words long.
#         If a process is asked, provide a step-by-step solution. Make sure the final response is clear, comprehensive, and customer-friendly.
#         Once you have generated a response, you will send it to the JSON formatter so that it can format the response into a JSON file.
#     ''',
#     expected_output='A detailed and well-formatted customer care response, including explanations for tough words and step-by-step solutions where applicable.',
#     tools=[net_tool],
#     agent=writer_agent,
# )


# json_conversion_task = Task(
#     description='Convert the questions and answers into a JSON file with keys "question" and "answer". You will fetch the questions from customer inquiry task and answers from writer task.',
#     expected_output='A JSON file with keys "question" and "answer".',
#     tools=[net_tool],
#     agent=json_converter_agent,
#     async_execution=False,
#     output_file='questions.json',
# )
customer_inquiry_task = Task(
    description='''Generate questions about {topic} in the first-person perspective, simulating how a customer might ask them.
    For example, if the topic is related to car maintenance, a question might be "My steering wheel is making noise; what should I do?".
    For each {topic}, generate a sequence of follow-up questions from the customer's perspective.
    Once you have generated a question, send it to the formatter so that it can format the question into a JSON file.
    ''',
    expected_output='A list of first-person questions from the customer for each topic.',
    tools=[net_tool],
    agent=customer_agent,
)

technical_support_task1 = Task(
    description='Answer the customer’s questions about {topic} using the provided vehicle’s owner manual.',
    expected_output='Answers to the customer’s questions for each topic.',
    tools=[pdf_reader_tool],
    agent=tech_support_agent1,
)

technical_support_task2 = Task(
    description='Answer the customer’s questions about {topic} using the provided vehicle’s owner manual.',
    expected_output='Answers to the customer’s questions for each topic.',
    tools=[pdf_reader_tool],
    agent=tech_support_agent2,
)

writing_task = Task(
    description='''
        Combine and refine answers from technical support agents about {topic} into a well-formatted customer care response.
        Ensure the response is detailed and includes explanations for any tough or technical terms. The response should be at least 100 words long.
        If a process is asked, provide a step-by-step solution. Make sure the final response is clear, comprehensive, and customer-friendly.
        Once you have generated a response, you will send it to the JSON formatter so that it can format the response into a JSON file.
    ''',
    expected_output='A detailed and well-formatted customer care response, including explanations for tough words and step-by-step solutions where applicable, for each topic.',
    tools=[net_tool],
    agent=writer_agent,
)

json_conversion_task = Task(
    description='''
        Convert the questions and answers into a JSON file with keys "question" and "answer" for each topic.
        Collect questions from the customer inquiry task and answers from the writing task for each topic, and pair them accordingly.
    ''',
    expected_output='A JSON file with keys "question" and "answer" for each topic.',
    tools=[net_tool],
    agent=json_converter_agent,
    async_execution=False,
    output_file='questions.json',
)
