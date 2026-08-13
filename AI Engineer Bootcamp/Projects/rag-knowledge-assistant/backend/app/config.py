import os

from dotenv import load_dotenv


load_dotenv(".env.local")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "company_knowledge_v2"

GEMINI_MODEL = "gemini-2.5-flash"