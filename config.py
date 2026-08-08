import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

load_dotenv()

username = quote_plus(os.getenv("DB_USER", ""))
password = quote_plus(os.getenv("DB_PASSWORD", ""))
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
database = os.getenv("DB_NAME", "")


DATABASE_URL = (f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

engine = create_engine(DATABASE_URL)
