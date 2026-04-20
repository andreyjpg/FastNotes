from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

sqlite_url = os.getenv("DATABASE_URL")
print(sqlite_url)
engine = create_engine(sqlite_url)

def get_session():
    with Session(engine) as session:
        yield session  
