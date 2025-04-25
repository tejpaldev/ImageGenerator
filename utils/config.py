import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Together API model name
TOGETHER_MODEL = "black-forest-labs/FLUX.1-schnell"
