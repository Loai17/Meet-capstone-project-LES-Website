from sqlalchemy import Column,Date,Integer,String,Boolean, DateTime, ForeignKey, Float
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

class Newsletter(Base):
    __tablename__="newsletter"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True)
    email = Column(String(255))

class Forums(Base):
    __tablename__="forums"
    __table_args__={'extend_existing':True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users")
    title = Column(String(255))
    description = Column(String)

class Games(Base):
    __tablename__="games"
    __table_args__={'extend_existing' : True}
    id = Column(Integer,primary_key=True)
    name=Column(String)
    smallDes=Column(String)
    description=Column(String)

class ContactUs(Base):
    __tablename__="contactUs"
    __table_args__={'extend_existing':True}
    id=Column(Integer,primary_key=True)
    name = Column(String)
    email = Column(String)
    message = Column(String)
 #   press = Column(Boolean)
#    customer = Column(Boolean)

class ForumComments(Base):
    __tablename__="Forum Comments"
    __table_args__={'extend_existing':True}
    id=Column(Integer,primary_key=True)
    comment= Column(String)
    forum_id= Column(Integer)
    userNameF = Column(String)

class GameComments(Base):
    __tablename__="Game Comments"
    __table_args__={'extend_existing':True}
    id=Column(Integer,primary_key=True)
    comment= Column(String)
    game_id= Column(Integer)
    userNameG = Column(String)


def hash_password(password):
    password = pwd_context.encrypt(password)

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()