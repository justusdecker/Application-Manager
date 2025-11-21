from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text

from sqlalchemy.exc import IntegrityError

DATABASE_PATH = f'./data.db'
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
Base = declarative_base()

class JobApplianceStates:
    INVALID = -1
    NOT_APPLIED = 0
    APPLIED = 1
    SCREEN = 2
    INTERVIEW = 3
    OFFER = 4
    DENIED = 5

class JobIds(Base):
    __tablename__ = "JobIds"
    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable = False)
    
class Jobs(Base):
    __tablename__ = "Jobs"
    id = Column(Integer, primary_key=True)
    company = Column(String, nullable = False)
    title_id = Column(Integer, nullable = False)
    url = Column(String, nullable = False)
    mail = Column(String)
    phone_number = Column(String)
    description = Column(String)
    state = Column(Integer, default=JobApplianceStates.NOT_APPLIED)

class JobTitle:
    __tablename__ = "JobTitle"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable = False)

class ApplicationPreset:
    __tablename__ = "ApplicationPreset"
    id = Column(Integer, primary_key=True)
    job_title_id = Column(Integer, nullable = False)
    
def connect() -> tuple[Engine, Session]:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return engine, session

ENGINE, SESSION = connect()

def tcom():
    try:
        SESSION.commit()
        return True
    except IntegrityError as E:
        print(E)
        return False

def get_job_id(key: str):
    return SESSION.query(JobIds).filter_by(name = key).one().id

def get_job_names() -> list[str]:
    return [e.name for e in SESSION.query(JobIds)]

def add_job_id(job_id: JobIds):
    SESSION.add(job_id)
    return tcom()

def add_job(job: Jobs) -> bool:
    SESSION.add(job)
    return tcom()