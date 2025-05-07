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
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://gestion_obras_user:GRMyMNzYVSV6agxrbG6EQYYZ48ws73Lu@dpg-d0dbfgjuibrs73f5mqvg-a.oregon-postgres.render.com/gestion_obras")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
