# import fitz  # PyMuPDF
from crewai import Crew, Process
from agents import tech_support_agent1,tech_support_agent2, customer_agent, writer_agent, json_converter_agent
from tasks import customer_inquiry_task, technical_support_task1, technical_support_task2, writing_task, json_conversion_task


# Initialize the crew with the defined tasks
crew = Crew(
    agents=[customer_agent, tech_support_agent1, tech_support_agent2, writer_agent, json_converter_agent],
    tasks=[customer_inquiry_task, technical_support_task1, technical_support_task2, writing_task, json_conversion_task],
    process=Process.sequential
)

# Define the topics to be covered
topics = ['steering wheel', 'brakes', 'engine']  # Example topics
inputs_array = [{'topic': 'steering wheel'}, {'topic': 'brakes'}, {'topic': 'engine'}]
# inputs_array = [{'topic': 'steering wheel'}]
# Run the custom process
result = crew.kickoff_for_each(inputs=inputs_array)