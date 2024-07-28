from crewai_tools import PDFSearchTool
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')


# Initialize the tool allowing for any PDF content search if the path is provided during execution
pdf_reader_tool = PDFSearchTool(pdf="punch.pdf",
    config=dict(
        llm=dict(
            provider="groq", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama3-8b-8192",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="huggingface", # or openai, ollama, ...
            config=dict(
                model="BAAI/bge-small-en-v1.5",
                #task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
from crewai_tools import SerperDevTool

# Initialize the tool for internet searching capabilities
net_tool = SerperDevTool()