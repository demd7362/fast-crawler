import databases
import sqlalchemy
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, declarative_base

from app.base.Bases import Base

print('database configuration...')
DATABASE_URL = "mysql://jhjh:Wjd999888!@144.24.74.58:3306/FC"
database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)



def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()



