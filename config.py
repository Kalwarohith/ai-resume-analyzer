import os

class Config:
    SECRET_KEY = "supersecretkey"
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB