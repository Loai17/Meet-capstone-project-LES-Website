from sqlalchemy import Column,Date,Integer,String,Boolean, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

from databaseSetup import Base , Users , Newsletter , Forums , Games , ContactUs

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)#, autoflush=False)
session = DBSession()

loai=Users(firstName="Loai",lastName="Qubti",userName="Loaiq1107",password="12345",
    email="loai.qubti@gmail.com",photo="Implement later",dob= datetime(2000, 7, 11),description="I'm doing this website yay!")

subscribe1=Newsletter(email = "loai.qubti@gmail.com")
post = Forums(title="Hi",user_id=1,description="Bye")
territory=Games(name="Territory",smallDes="Plant 5 trees w/ each purchase",description="cool game discription yooooooooo")
welterBrothers=Games(name="Welter Brothers",smallDes="Fight the zombie apocalypse seperated",description="YOu two are seperated lol")
contacter=ContactUs(name="Customer Yo",email="some1@gmail.com",message="Nice games")#,press=False,customer=True)
session.query(Users).delete()
session.query(Newsletter).delete()
session.query(Forums).delete()
session.query(Games).delete()
session.query(ContactUs).delete()
session.add(contacter)
session.add(territory)
session.add(welterBrothers)
session.add(loai)
session.add(subscribe1)
session.add(post)
session.commit()