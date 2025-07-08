import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "therapydb")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")
    OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434")
    STRIPE_KEY = os.getenv("STRIPE_KEY")
