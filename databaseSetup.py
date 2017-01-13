from sqlalchemy import Column,Date,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    lastName = Column(String(255))
    userName = Column(String(255), unique=True)
    password = Column(String(255))
    email = Column(String(255), unique=True)
    photo = Column(String)
    dob = Column(Date)
    description = Column(String)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

class Newspaper(Base):
    __tablename__="newspaper"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True)
    email = Column(String(255))

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

loai=Users(firstName="Loai",lastName="Qubti",userName="Loaiq1107",password="12345",
    email="loai.qubti@gmail.com",photo="Implement later",dob= datetime(2000, 7, 11),description="I'm doing this website yay!")

subscribe1=Newspaper(email = "loai.qubti@gmail.com")

session.query(Users).delete()
session.query(Newspaper).delete()
session.add(loai)
session.add(subscribe1)
session.commit()