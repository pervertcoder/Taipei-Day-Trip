import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SECRET_KEY = os.getenv('SECRET_KEY')

PARTNER_KEY = os.getenv('PARTNER_KEY')

ALGORITHM = 'HS256'