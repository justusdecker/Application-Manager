from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from src.validation import integer_or_default
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from src.validation import integer_or_default

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
    state_id = Column(Integer, default=JobApplianceStates.NOT_APPLIED)

class LinkedInJobsTable(Base):
    __tablename__ = "LinkedInJobs"
    id = Column(Integer, primary_key=True)
    lid = Column(String)
    company = Column(String, nullable = False)
    job_title = Column(String, nullable = False)
    logo = Column(String, nullable = False)
    description = Column(String, nullable = False)
    
class CVCTable(Base):
    __tablename__ = "CVCS"
    id = Column(Integer, primary_key=True)
    cvc = Column(String, nullable= False)
    name = Column(String, nullable= False)

def _get_state_as_text(id: int) -> str:
    for key, val in JobApplianceStates.get():
        if id == val:
            return key

class SQL:
    """
    A generic wrapper for CRUD operations (Create, Read, Update, Delete)
    on a specific SQLAlchemy model.
    """
    def __init__(self, 
                 SESSION: Session,
                 TABLE):
        self.SESSION: Session = SESSION
        self.TABLE = TABLE
        
    def read(self, id: int | str):
        """
        Retrieves a record by its ID.

        Behavior:
            Uses `validate_id_and_get`. If the provided ID is invalid or 
            cannot be found, this method falls back to returning the 
            last (newest) entry in the table.

        Args:
            id (int | str): The ID to search for.

        Returns:
            Object | None: The found database object or the last entry as fallback.
                           Returns None if the table is empty.
        """
        return self.validate_id_and_get(id)

    def create(self, **data):
        """
        Creates a new record.

        Args:
            **data: Keyword arguments matching the column names of the table.

        Returns:
            bool: True if successful, None if an error occurred (e.g., IntegrityError).
        """
        self.SESSION.add(self.TABLE(**data))
        return self.commit()

    def delete(self, id: int | str):
        """
        Deletes a record by its ID.

        Safety:
            Unlike `read`, this method performs NO fallback. If the ID does 
            not exist exactly, nothing happens. This prevents accidental 
            deletion of wrong data.

        Args:
            id (int | str): The ID of the record to delete.

        Returns:
            bool: True if commit was successful, None on database error.
            None: If the ID was not found.
        """
        clean_id = integer_or_default(id, -1)
        entry = self.SESSION.get(self.TABLE, clean_id)
        
        if entry is None: return None
        
        self.SESSION.delete(entry)
        return self.commit()

    def update(self, id: int | str, **data):
        """
        Updates an existing record.

        Safety:
            Like `delete`, this method performs NO fallback. Only exact ID matches
            will be updated.

        Args:
            id (int | str): The ID of the record to update.
            **data: The fields to update (key=value). Keys that do not exist 
                    in the model are ignored.

        Returns:
            bool: True if commit was successful (or nothing changed).
            None: If the ID was not found.
        """
        clean_id = integer_or_default(id, -1)
        entry = self.SESSION.get(self.TABLE, clean_id)
        
        if entry is None: 
            return None

        for key, value in data.items():
            if hasattr(entry, key):
                if getattr(entry, key) != value:
                    setattr(entry, key, value)
   
        return self.commit()
    
    def commit(self) -> bool:
        """
        Executes the database commit and handles errors.

        Returns:
            bool: True on success, None on error (triggers rollback).
        """
        try:
            self.SESSION.commit()
            return True
        except IntegrityError as e:
            self.SESSION.rollback()
            print(f"IntegrityError: {e}")
            return None
    
    def validate_id_and_get(self, id: str):
        """
        Attempts to safely retrieve an object (with fallback logic).

        Logic:
        1. Tries to convert the ID to an integer.
        2. Tries to load the object directly via Primary Key (Fast).
        3. If 1 or 2 fails: Loads the last (newest) entry of the table as a fallback.

        Args:
            id (str | int): The raw ID.

        Returns:
            Object | None: The found object or None if table is empty/error.
        """
        clean_id = integer_or_default(id, -1)
        #1. Try(Fast)
        if clean_id != -1:
            entry = self.SESSION.get(self.TABLE, clean_id)
            if entry:
                return entry
            
        try:
            return self.SESSION.query(self.TABLE).order_by(self.TABLE.id.desc()).first()
        except Exception:
            return None
    
class JobIds(SQL):
    """
    Specialized Class for JobId-Operations.
    Inherits all CRUD-Functions from SQL & expand it by JobId-specific logic.
    """
    def __init__(self, SESSION, TABLE):
        super().__init__(SESSION, TABLE)
        
    def create(self, name: str) -> bool:
        """Creates a new job with the given name"""
        return super().create(name=name)
    
    def update(self, id, **data):
        """Updates the name of a job."""
        return super().update(id, **data)
    
    def read_all(self, as_dict: bool = False) -> list:
        """
        Reads all jobs.
        
        if as_dict: gives you a list[dict]
        else: gives you a list[SQLTable]
        
        """
        query = self.SESSION.query(self.TABLE).all()
        
        if as_dict:
            return [self._to_dict(entry) for entry in query]
        return query
    
    def read_as_dict(self, id: int | str) -> dict | None:
        """Reads a single jb & returns it as dictionary"""
        entry = self.read(id)
        if entry is None:
            return None
        return self._to_dict(entry)
    
    def get_job_name(self, id: int | str) -> str | None:
        """
        Gets only the job name corresponding to the id
        """
        entry = self.read(id)
        if entry:
            return entry.name
        return None

    def get_ids(self) -> list[int]:
        """Gets the list of existing ids"""
        return [res[0] for res in self.SESSION.query(self.TABLE.id).all()]

    def get_last_entry(self):
        """Gets the last(newest) JobId-Object."""
        try:
            return self.SESSION.query(self.TABLE).order_by(self.TABLE.id.desc()).first()
        except Exception:
            return None

    def _to_dict(self, entry) -> dict:
        """Internal Helper: Converts SQLAlchemy Object to dict."""
        
        return {k: v for k, v in entry.__dict__.items() if not k.startswith('_')}

class Jobs(SQL):
    """
    Specialized Class for Job-Operations.
    Inherits all CRUD-Functions from SQL and expand these by Job-Logic.
    """

    def __init__(self, SESSION, TABLE):
        super().__init__(SESSION, TABLE)
    
    def create(self, 
               company: str, 
               title_id: int, 
               url: str, 
               mail: str = None, 
               phone_number: str = None, 
               description: str = None, 
               state_id: int = JobApplianceStates.NOT_APPLIED) -> bool:
        """
        Creates a new job-entry.
        ### Valid data:

            company: str, 
            title_id: int, 
            url: str, 
            mail: str, 
            phone_number: str, 
            description: str, 
            state_id: int
        """
        return super().create(**{
            'company': company,
            'title_id': title_id,
            'url': url,
            'mail': mail,
            'phone_number': phone_number,
            'description': description,
            'state_id': state_id})
    
    def update(self, id: int | str, **data) -> bool | None:
        """
        Updates the Job-Entry
        
        ### Valid data:

            company: str, 
            title_id: int, 
            url: str, 
            mail: str, 
            phone_number: str, 
            description: str, 
            state_id: int
        """
        return super().update(id, **data)


    def read_all(self, as_dict: bool = False, job_id_instance: JobIds = None) -> list:
        if job_id_instance is None: return []
        """Reads all job-entrys"""
        query = self.SESSION.query(self.TABLE).all()
        
        if as_dict:
            return [self.read_as_dict(entry.id, job_id_instance) for entry in query]
        return query

    def read_as_dict(self, id: int | str, job_id_instance: JobIds) -> dict | None:
        """
        Reads a single job-entry and returns it as dict.
        Returns None if id does not exist
        """
        entry = self.read(id)
        if entry is None:
            return None
            
        data = self._to_dict(entry)
        try:
            title = job_id_instance.get_job_name(data['title_id'])
            state = _get_state_as_text(data['state_id'])
            
            data['title'] = title
            data['state'] = state
        except Exception as e:
            data['title'] = data.get('title', '')
            data['state'] = data.get('state', '')
            print(f"Warning: Error while data enrich: {e}, using default \"\"")
            
        return data

    def get_last_id(self) -> int | None:
        """Returns the last id in the table or None"""
        try:
            last_entry = self.SESSION.query(self.TABLE.id).order_by(self.TABLE.id.desc()).first()
            return last_entry[0] if last_entry else None
        except Exception:
            return None
            
    def _to_dict(self, entry) -> dict:
        """
        Internal Helper: Converts SQLAlchemy Object to dict
        """
        
        return {k: v for k, v in entry.__dict__.items() if not k.startswith('_')}

class LinkedInJobs(SQL):
    """
    Specialized Class for LinkedInJob-Operations.
    Inherits all CRUD-Functions from SQL and expand these by LinkedInJob-Logic.
    """

    def __init__(self, SESSION, TABLE):
        super().__init__(SESSION, TABLE)
    
    def create(self, 
               company: str, 
               job_title: int,
               lid: str, 
               description: str,
               logo: str) -> bool:
        """
        Creates a new linkedInjob-entry.
        ### Valid data:

            company: str, 
            job_title: int,
            lid: int, 
            description: str,
            logo: str
        """
        #if self.is_lid_inthere(lid):
        #    return False
        return super().create(**{
            'company': company,
            'job_title': job_title,
            'lid': lid,
            'logo': logo,
            'description': description})
    
    def update(self, id: int | str, **data) -> bool | None:
        """
        Updates the LinkedInJob-Entry
        
        ### Valid data:

            company: str, 
            job_title: int,
            lid: int, 
            description: str,
            logo: str
        """
        return super().update(id, **data)


    def read_all(self, as_dict: bool = False) -> list:
        """Reads all LinkedInjob-entrys"""
        query = self.SESSION.query(self.TABLE).all()
        
        if as_dict:
            return [self.read_as_dict(entry.id) for entry in query]
        return query

    def read_as_dict(self, id: int | str) -> dict | None:
        """
        Reads a single LinkedInjob-entry and returns it as dict.
        Returns None if id does not exist
        """
        entry = self.read(id)
        if entry is None:
            return None
            
        data = self._to_dict(entry)
        return data

    def is_lid_inthere(self, lid) -> bool:
        entry = self.SESSION.query(self.TABLE).get({'lid':lid})

        return False if entry is None else True
    
    def get_last_id(self) -> int | None:
        """Returns the last id in the table or None"""
        try:
            last_entry = self.SESSION.query(self.TABLE.id).order_by(self.TABLE.id.desc()).first()
            return last_entry[0] if last_entry else None
        except Exception:
            return None
            
    def _to_dict(self, entry) -> dict:
        """
        Internal Helper: Converts SQLAlchemy Object to dict
        """
        
        return {k: v for k, v in entry.__dict__.items() if not k.startswith('_')}


class CVC(SQL):
    """
    Specialized Class for CV-Operations.
    Inherits all CRUD-Functions from SQL and expand these by CV-Logic.
    """

    def __init__(self, SESSION, TABLE):
        super().__init__(SESSION, TABLE)
    
    def create(self, cvc: str) -> bool:
        """
        Creates a new CV-entry.
        ### Valid data:

            cvc: str
        """
        return super().create(**{'cvc': cvc})
    
    def update(self, id: int | str, **data) -> bool | None:
        """
        Updates the CV-Entry
        
        ### Valid data:
            cvc: str
        """
        return super().update(id, **data)


    def read_all(self, as_dict: bool = False) -> list:
        """Reads all CV-entrys"""
        query = self.SESSION.query(self.TABLE).all()
        
        if as_dict:
            return [self.read_as_dict(entry.id) for entry in query]
        return query

    def read_as_dict(self, id: int | str) -> dict | None:
        """
        Reads a single CV-entry and returns it as dict.
        Returns None if id does not exist
        """
        entry = self.read(id)
        if entry is None:
            return None
            
        data = self._to_dict(entry)
        return data
    
    def get_last_id(self) -> int | None:
        """Returns the last id in the table or None"""
        try:
            last_entry = self.SESSION.query(self.TABLE.id).order_by(self.TABLE.id.desc()).first()
            return last_entry[0] if last_entry else None
        except Exception:
            return None
            
    def _to_dict(self, entry) -> dict:
        """
        Internal Helper: Converts SQLAlchemy Object to dict
        """
        
        return {k: v for k, v in entry.__dict__.items() if not k.startswith('_')}


def connect() -> tuple[Engine, Session]:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return engine, session

ENGINE, SESSION = connect()
JOBS = Jobs(SESSION, JobsTable)
JOBIDS = JobIds(SESSION, JobIdsTable)
LJOBS = LinkedInJobs(SESSION, LinkedInJobsTable)
CVCS = CVC(SESSION, CVCTable)