from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:<password@localhost/task_manager"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

