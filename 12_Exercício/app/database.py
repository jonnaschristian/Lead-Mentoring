from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:desenvolvedor.py22@localhost/mentoria')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():     
    db = SessionLocal()
    try:         
        yield db     
    finally:
        db.close()
       