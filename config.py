import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}

MAX_CONTENT_LENGTH = 10 * 1024 * 1024

GROQ_API_KEY = os.getenv("GROQ_API_KEY")