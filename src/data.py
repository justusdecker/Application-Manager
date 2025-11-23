from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.validation import integer_or_default
from typing import Any, List, Self

DATABASE_PATH = f'./data.db'
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
Base = declarative_base()

def remove_unused(obj) -> dict:
    d: dict[str, Any] = obj.__dict__
    return {e: d[e] for e in d if not e.startswith('_')}

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
    state_id = Column(Integer, default=JobApplianceStates.NOT_APPLIED)

class JobTitleTable:
    __tablename__ = "JobTitle"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable = False)

class ApplicationPresetTable:
    __tablename__ = "ApplicationPreset"
    id = Column(Integer, primary_key=True)
    job_title_id = Column(Integer, nullable = False)
    
def validate_id(id: str, table) -> int | None:
    """
    Validates and sanitizes a string ID for database lookup.

    This function attempts to convert the input ID string to an integer. 
    If the conversion fails or results in a default invalid value (e.g., -1 
    from `integer_or_default`), the ID is set to the index of the last record 
    in the `table` (i.e., `count - 1`).

    Args:
        id: The string ID to be validated.
        table: The table to lookup

    Returns:
        The validated integer ID, which will be the ID of an existing job entry.
        
        Returns **None** if the `JobsTable` is completely empty.
    """
    l = SESSION.query(table).count()
    if not l: return None
    id = integer_or_default(id, -1)
    if id == -1: 
        id = l
    return id

def _get_state_as_text(id: int) -> str:
    for key, val in JobApplianceStates.get():
        if id == val:
            return key

class SQL:

    def read(table, id: int | str, query = None):
        id = validate_id(id, table)
        data = None
        if id is None: return None
        
        query =  SESSION.query(table) if query is None else query
        try:
            data = query.filter_by(id = id).one()
        except NoResultFound: 
            print(f'NoResultFound in {table.__tablename__}')
        return data

    def create(table, **data):
        SESSION.add(table(**data))
        return tcom()

    def delete(table, id: int | str):
        print(id)
        id = validate_id(id, table)
        if id is None: return None
        print(id)
        r = SQL.read(table, id)
        if r is None: return None
        
        SESSION.delete(r)
        return tcom()

    def update(table, id: int | str, **data) -> bool:
            id = validate_id(id, table)
            if id is None: return None
            old = SQL.read(table, id)
            if old is None: 
                return None

            for e in remove_unused(old):
                if e in data:
                    setattr(old, e, data[e])
                    print(old.__dict__[e], data[e])
            return tcom()

class Job:
    
    
    def create(company: str,
                 title_id: int,
                 url: str,
                 mail: str = None,
                 phone_number: str = None,
                 description: str = None,
                 state_id: int = JobApplianceStates.NOT_APPLIED):
        return SQL.create(JobsTable,**{
            'company': company,
            'title_id': title_id,
            'url': url,
            'mail': mail,
            'phone_number': phone_number,
            'description': description,
            'state_id': state_id})
    
    def read_all(as_type: bool = False) -> list[JobsTable] | list[dict[str, Any]]:
        q = SESSION.query(JobsTable)
        l = q.all()
        if as_type:
            return [Job.read_as_sql(i.id, q) for i in l]
        else:
            return [Job.read_as_dict(i.id, q) for i in l]

    def read_as_sql(id: str | int, query = None) -> JobsTable:
        return SQL.read(JobsTable, id, query)
    
    def read_as_dict(id: str | int, query = None) -> dict:
        data = SQL.read(JobsTable, id, query)
        if data is None: return None
        data = remove_unused(data)
        title = JobID._get_job_name(data['title_id'])
        state = _get_state_as_text(id)
        data |= {'title': title, 'state': state}
        return data

    def update(id: int | str, name: str):
        return SQL.update(JobsTable, id, **{'name': name})
    
    def delete(id: str | int):
        return SQL.delete(JobsTable, id)

    def get_last():
        return max([e.id for e in Job.read_all(True) if e is not None])

class JobID:
    def create(name: str):
        return SQL.create(JobIdsTable,**{'name': name})
    
    def read_all(as_type: bool = False) -> list[JobIdsTable] | list[dict[str, Any]]:
        q = SESSION.query(JobIdsTable)
        l = q.all()
        if as_type:
            return [JobID.read_as_sql(i, q) for i in l]
        else:
            return [JobID.read_as_dict(i.id, q) for i in l]

    def read_as_sql(id: str | int, query = None) -> JobIdsTable:
        return SQL.read(JobIdsTable, id, query)
    
    def read_as_dict(id: str | int, query = None) -> dict:
        data = SQL.read(JobIdsTable, id, query)
        if data is None: return None
        return remove_unused(data)

    def update(id: int | str, name: str):
        return SQL.update(JobIdsTable, id, **{'name': name})
    
    def delete(id: str | int):
        return SQL.delete(JobIdsTable, id)
    
    def _get_job_name(id: int):
        data = JobID.read_all()
        for j in data:
            if j['id'] == id:
                return j['name']
    
    def get_last():
        return max([e.id for e in JobID.read_all(True) if e is not None])

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

Job.create(
                company = "Test",
                description = "Nothing here",
                mail = "j@gmx.tv",
                phone_number = "+3118054646",
                state_id = 0,
                title_id = 0,
                url = "afa"
            
        )

Job.delete(-1)
JobID.create(name='123')
#JobID.update(1,name='test')
print(JobID.read_as_dict(2))
print(Job.read_all())