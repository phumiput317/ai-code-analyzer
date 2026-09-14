import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER", "phumiput317")
REPO = os.getenv("GITHUB_REPO", "HW03-65123317")
MODEL = "gemini-3.6-flash"
GITHUB_REQUEST_TIMEOUT = 10
MAX_REPOSITORY_FILES = 50
MAX_FILE_SIZE = 200_000
MAX_PROJECT_CHARS = 300_000

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Add it to your .env file.")