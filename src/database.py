from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://blog_user:blog_pass@lockalhost:5432/blog_db")

engine = create_engine(DATABASE_URL)
sessinlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
