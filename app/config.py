import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SERVER_PORT = int(os.environ.get("SERVER_PORT", 5555))
    API_ROOT = os.environ.get("API_ROOT", "/api")
    API_SUFFIX = os.environ.get("API_SUFFIX", "/v1")
    API_SWAGGERUI = os.environ.get("API_SWAGGERUI", "/docs")

    DB_SERVER = os.environ.get("DB_SERVER", "db_server")
    DB_NAME = os.environ.get("DB_NAME", "db_name")
    DB_USER = os.environ.get("DB_USER", "db_user")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "db_password")
    DB_HOST = os.environ.get("DB_HOST", "db_host")
    DB_PORT = os.environ.get("DB_PORT", "db_port")

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
    )
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    SECRET_KEY = os.environ.get("SECRET_KEY")
