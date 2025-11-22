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
    def get():
        return [
            ('INVALID', JobApplianceStates.INVALID),
            ('NOT_APPLIED', JobApplianceStates.NOT_APPLIED),
            ('APPLIED', JobApplianceStates.APPLIED),
            ('SCREEN', JobApplianceStates.SCREEN),
            ('INTERVIEW', JobApplianceStates.INTERVIEW),
            ('OFFER', JobApplianceStates.OFFER),
            ('DENIED', JobApplianceStates.DENIED)
        ]

class JobIdsTable(Base):
    __tablename__ = "JobIds"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    
class JobsTable(Base):
    __tablename__ = "Jobs"
    id = Column(Integer, primary_key=True)
    company = Column(String, nullable = False)
    title_id = Column(Integer, nullable = False)
    url = Column(String, nullable = False)
    mail = Column(String)
    phone_number = Column(String)
    description = Column(String)
    state = Column(Integer, default=JobApplianceStates.NOT_APPLIED)

class Job:
    def get_job_info(id: str) -> list[int, str]:
        l = SESSION.query(JobsTable).count()
        id = int(id)
        if id == -1:
            id = l - 1
        r = SESSION.query(JobsTable).filter_by(id = id).one()
        return [
            ('ID', r.id), 
            ('Company', r.company), 
            ('Title', r.title_id), 
            ('URL', r.url), 
            ('Mail', r.mail), 
            ('Phone Number', r.phone_number), 
            ('Description', r.description), 
            ('State',r.state)
        ]
    def get_job_info_obj(id: str) -> list[int, str]:
        l = SESSION.query(JobsTable).count()
        id = int(id)
        if id == -1:
            id = l - 1
        r = SESSION.query(JobsTable).filter_by(id = id).one()
        return {
            'id': r.id,
            'company': r.company,
            'job_title': JobID.get_job_name(r.title_id),
            'url': r.url,
            'mail': r.mail,
            'phone_number': r.phone_number,
            'description': r.description,
            'state': r.state
        }
    
    def update_job(id: int,
                   company,
            description,
            mail,
            phone_number,
            state,
            title_id,
            url
                   ):
        o = SESSION.query(JobsTable).filter_by(id = int(id)).one()
        o.company = company
        o.description = description
        o.mail = mail
        o.phone_number = phone_number
        o.state = int(state)
        o.title_id = int(title_id)
        o.url = url
        SESSION.commit()
    
    def get_all_jobs():
        return SESSION.query(JobsTable).all()
    
    def add_job(job: JobsTable) -> bool:
        SESSION.add(job)
        return tcom()

class JobID:
    def get_job_ids() -> list[JobIdsTable]:
        return SESSION.query(JobIdsTable).all()

    def get_job_id(key: str):
        return SESSION.query(JobIdsTable).filter_by(name = key).one().id
    
    def get_job_name(id: int):
        try:
            return SESSION.query(JobIdsTable).filter_by(id = id).one().name
        except:
            return 'None'
    
    def add_job_id(job_id: JobIdsTable):
        SESSION.add(job_id)
        return tcom()


class JobTitleTable:
    __tablename__ = "JobTitle"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable = False)

class ApplicationPresetTable:
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


def get_job_names() -> list[str]:
    return [e.name for e in SESSION.query(JobIdsTable)]
