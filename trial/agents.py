import os
from crewai import Agent
from tools import pdf_reader_tool
from net_tool import net_tool
from dotenv import load_dotenv
load_dotenv()

# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
#                              verbose=True,
#                              temperature=0.8,
#                              google_api_key=os.getenv("GOOGLE_API_KEY"))

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Define agents
customer_agent = Agent(
    role='Customer',
    goal='Ask questions about vehicle issues',
    backstory='You are a vehicle owner experiencing issues and need technical support.',
    verbose=True,
    memory=True,
    # llm = llm,
    tools=[net_tool],
    max_iter=10,
    allow_delegation=True
)

tech_support_agent1 = Agent(
    role='Technical Support Specialist',
    goal='Answer questions about vehicle issues using the owner’s manual',
    backstory='You are a knowledgeable technician experienced in handling vehicle issues.',
    # llm = llm,
    verbose=True,
    memory=True,
    tools=[pdf_reader_tool],
    max_iter=10,
    allow_delegation=True
)

tech_support_agent2 = Agent(
    role='Technical Support Specialist',
    goal='Answer questions about vehicle issues using the owner’s manual',
    backstory='You are a knowledgeable technician experienced in handling vehicle issues.',
    # llm = llm,
    verbose=True,
    memory=True,
    tools=[pdf_reader_tool],
    max_iter=10,
    allow_delegation=True
)

writer_agent = Agent(
    role='Customer Care Writer',
    goal='Combine and refine answers from technical support agents into a well-formatted customer care form.',
    backstory='You have a knack for writing clear and concise customer care responses.',
    # llm = llm,
    verbose=True,
    memory=True,
    tools=[net_tool],
    max_iter=10,
    allow_delegation=True
)

json_converter_agent = Agent(
    role='JSON Formatter',
    goal='Convert the questions and answers into a JSON file with keys "context", "question", and "answer".',
    backstory='You are responsible for ensuring all information is properly formatted in JSON.',
    # llm = llm,
    verbose=True,
    memory=True,
    tools=[net_tool],
    max_iter=10,
    allow_delegation=False
)