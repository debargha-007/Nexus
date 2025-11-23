# --------//  LLM and API configurations // -------- #
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# ----- LLM configuration
llm = ChatOpenAI(model="gpt-4o", temperature=0)
