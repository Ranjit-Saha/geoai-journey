import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:
    # 1. Fetch Variables
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # Safety Guard: Fail loudly if the password is missing
    # We need User, Pass, and Name to even start.
    required_vars = {
        "DB_USER": DB_USER,
        "DB_PASS": DB_PASS,
        "DB_NAME": DB_NAME
    }
    for key, value in required_vars.items():
        if not value:
            raise EnvironmentError(f"❌ CRITICAL: {key} missing in .env file!")

    # The 'Professional Handshake': Securely builds the DB string
    DB_URL = URL.create(
        drivername="postgresql",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
