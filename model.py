from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///Job.db')
Base = declarative_base()

# CREATING THE TABLE
class Job(Base):

    __tablename__ = 'person1'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    day = Column(String, nullable=False)
    hours = Column(String, nullable=False)
    tot_hours = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    tot_day = Column(Integer, nullable=False)
    tot_week = Column(Integer, nullable=False)
    

class MyJob(Base):

    __tablename__ = 'person2'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    day = Column(String, nullable=False)
    hours = Column(String, nullable=False)
    tot_hours = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    tot_day = Column(Integer, nullable=False)
    tot_week = Column(Integer, nullable=False)

Base.metadata.create_all(engine)
