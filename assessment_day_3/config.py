import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Add it to the .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)