import json
import PyPDF2
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.8,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))
from crewai import Agent, Task, Crew, Process

# Step 1: Reading the JSON File
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Step 2: Define the CrewAI Process

# Define JSON Reader Agent
json_reader = Agent(
    role='JSON Reader',
    goal='Read and extract questions and answers from the JSON file.',
    verbose=True,
    memory=True,
    llm=llm,
    backstory='You are proficient in reading and parsing JSON data to extract relevant information.'
)

# Define PDF Analyzer Agent
pdf_analyzer = Agent(
    role='PDF Analyzer',
    goal='Identify the heading of each answer in the PDF document.',
    verbose=True,
    memory=True,
    llm=llm,
    backstory='You excel at analyzing PDF documents and extracting structured information.'
)

# Task to load JSON data
def load_json_task(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Task to find PDF headings
def find_pdf_headings_task(questions_answers, pdf_file_path):
    headings = []
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for qa in questions_answers:
            answer = qa['response']
            heading_found = False
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                if answer in text:
                    heading = text.split('\n')[0]  # Assuming the first line is the heading
                    headings.append({
                        "prompt": qa['prompt'],
                        "response": qa['response'],
                        "heading": heading
                    })
                    heading_found = True
                    break
            if not heading_found:
                headings.append({
                    "prompt": qa['prompt'],
                    "response": qa['response'],
                    "heading": "Heading not found"
                })
    return headings

# Creating tasks
load_json = Task(
    description='Read the JSON file and extract the questions and answers.',
    expected_output='A list of questions and corresponding answers.',
    agent=json_reader,
    tools=[load_json_task]
)

find_headings = Task(
    description='For each answer, locate the section heading in the PDF from which the answer was derived.',
    expected_output='A list of headings corresponding to each answer.',
    agent=pdf_analyzer,
    tools=[find_pdf_headings_task]
)

# Forming the crew
crew = Crew(
    agents=[json_reader, pdf_analyzer],
    tasks=[load_json, find_headings],
    process=Process.sequential
)

# Step 3: Function to execute the crew
def execute_crew(json_file_path, pdf_file_path, output_file_path):
    questions_answers = load_json_task(json_file_path)
    result = find_pdf_headings_task(questions_answers, pdf_file_path)
    with open(output_file_path, 'w') as output_file:
        json.dump(result, output_file, indent=4)
    return result

# Example usage
json_file_path = 'final.json'
pdf_file_path = 'punch.pdf'
output_file_path = 'output.json'

result = execute_crew(json_file_path, pdf_file_path, output_file_path)
print(f"Output written to {output_file_path}")
