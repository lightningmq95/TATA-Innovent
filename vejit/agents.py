import os
from crewai import Agent
from tools import pdf_reader_tool, net_tool
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.8,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

question_checker = Agent(
    role='Question Checker',
    goal='Validate questions based on work ethics and related topics.',
    backstory='You ensure that only appropriate and relevant questions proceed for answer generation.',
    llm = llm,
    max_iter = 5
)

answer_generator = Agent(
    role='Answer Generator',
    goal='Generate answers using a custom-trained model with confidence scores.',
    backstory='You provide answers with confidence scores, ensuring the reliability of the information.',
    llm = llm,
)

frag = Agent(
    role='Frag',
    goal='Use RAG to fetch answers from documents if the model\'s confidence is low.',
    backstory='You provide reliable answers by retrieving information from documents using RAG when the initial model confidence is low.',
    llm = llm,
    tools = [pdf_reader_tool],
)

crag = Agent(
    role='Crag',
    goal='Search the internet for answers if Frag fails, including a disclaimer about potential inaccuracies.',
    backstory='You search the internet for answers and provide a disclaimer about the potential for inaccuracies when the model confidence is low.',
    llm = llm,
    tools = [net_tool],
)