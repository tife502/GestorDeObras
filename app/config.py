import os
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://usuario:password@localhost:5432/sistemasdeobras")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
