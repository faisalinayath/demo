from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base=declarative_base()

class Person(Base):
    __tablename__="people"
    ssn=Column("ssn",Integer,primary_key=True)
    firstname=Column("firstname",String)
    lastname=Column("lastname",String)
    gender=Column("gender",CHAR)
    age=Column("age",Integer)

    def __init__(self,ssn,firstname,lastname,gender,age):
        self.ssn=ssn
        self.firstname=firstname
        self.lastname=lastname
        self.gender=gender
        self.age=age

    def __repr__(self):
        return f"({self.ssn}{self.firstname}{self.lastname}{self.gender}{self.age})"
    
# Replace the placeholders with your actual database credentials
username = 'postgres'
password = 'Fai2001#'
host = 'localhost'
port = '5432'
database = 'TUTORIAL_DB'

# PostgreSQL connection string format: postgresql://username:password@host:port/database
connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)
Base.metadata.create_all(bind=engine)

 #the above code creates a table in postgres db

Session=sessionmaker(bind=engine)
session=Session()

person=Person(1231,"faisal","Inayath","m",22)
session.add(person)
session.commit()

result=session.query(Person).all()
for r in result:
    print(r)

results=session.query(Person).filter(Person.lastname=="inayath")
for r in results:
    print(r)