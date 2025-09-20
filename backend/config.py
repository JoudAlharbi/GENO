import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
    PROJECT_ENV = os.getenv("PROJECT_ENV", "dev")
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "700"))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024