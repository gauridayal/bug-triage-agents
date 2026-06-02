"""
config.py
Loads environment variables and creates the shared LLM model object.
Every agent imports the model from here — one place to change it.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the .env file (your API keys)
load_dotenv()

# Read values from .env
API_KEY = os.getenv("OPENAI_API_KEY", "Notrequired")
BASE_URL = os.getenv("OPENAI_API_BASE_URL", "http://172.30.81.52:9000/v1")
MODEL_NAME = os.getenv("OPENAI_MODEL", "Qwen/Qwen3-Coder-30B-A3B-Instruct")

# Create the model — this connects to your office's Qwen server
# ChatOpenAI works with any OpenAI-compatible API (including your office server)
def get_model():
    return ChatOpenAI(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.1,       # Low temperature = more consistent responses
        max_tokens=2048,
    )

# Quick sanity check — run: python config.py
if __name__ == "__main__":
    model = get_model()
    response = model.invoke(
        "Say 'Connection successful!' and nothing else."
    )
    print("Model response:", response.content)