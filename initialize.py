from sqlalchemy import Column,Date,Integer,String,Boolean, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

from databaseSetup import Base , Users , Newsletter , Forums , Games , ContactUs , ForumComments , GameComments

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


def hash_password(password):
    password = pwd_context.encrypt(password)

loai=Users(firstName="Loai",lastName="Qubti",userName="Loaiq1107",password=hash_password("12345"),
    email="loai.qubti@gmail.com",photo="Implement later",dob= datetime(2000, 7, 11),description="I'm doing this website yay!")

subscribe1=Newsletter(email = "loai.qubti@gmail.com")
post = Forums(title="Hi",user_id=1,description="Bye")
territory=Games(name="Territory",smallDes="Territory indirectly teaches it's players how important trees are , in the game they'll start having no food or wood to build ,therefore in real life they'll start caring more about trees and actually realize what happens when only 1 tree gets cut down.",
description="GAME STORY : You live on an island , build what you need from it's trees (reasonably) , eat from it's fruit , and drink from the ocean around. Until one day , a ship full of people comes and decides to move in to the island. They start cutting down a lot of trees excessively to free up space and build houses. With trees being cut down you start losing resources and can't really keep building your essentials to live , nor eat and live on their fruit. You will have to start defending your island and what's on it to mark it as your territory by fighting the enemies , plant trees , and using the island resources (trees,fruit,water..etc) reasonably.    Where will The game be available (and what's special about it) : Territory will be on steam greenlight soon , and when launched , with each game purchase, 5 trees will be planted by donating money to special trees organizations.    Funding : We launched a crowdfunding campaign until 16 Feb, and it ended successfully with a total funding of $550 (which was the goal!) , and we'll start moving again properly now with our funds! So stay up to date by subscribing to us on our website , following us on twitter , or following our gamejolt devlog!" 
, image_url = "https://m.gjcdn.net/game-thumbnail/300/213942-scccrrxu.jpg")
welterBrothers=Games(name="Welter Brothers",smallDes="A top-down shooter game , where there are 2 soldiers , and a wall between them keeping them separated.",description="Game Story : 'Welter Brothers' is a top-down shooter game , where there are 2 soldiers , and a wall between them keeping them separated. At the time they happen to be separated , a zombie apocalypse begins. You should keep both brothers alive , by controlling them and shooting the zombies. You can use only one brother at a time , you cant play with both. Each round there are more zombies." , image_url="https://m.gjcdn.net/game-thumbnail/300/221440-crop0_0_1919_1080-jxk6rjvf.jpg")
contacter=ContactUs(name="Customer Yo",email="some1@gmail.com",message="Nice games")#,press=False,customer=True)
forum_cmnt=ForumComments(comment="Nice post!",forum_id=1,userNameF='Loaiq1107')
game_cmnt=GameComments(comment="Nice Game!",game_id=1,userNameG='Loaiq1107')
session.query(Users).delete()
session.query(Newsletter).delete()
session.query(Forums).delete()
session.query(Games).delete()
session.query(ContactUs).delete()
session.query(ForumComments).delete()
session.query(GameComments).delete()
session.add(contacter)
session.add(territory)
session.add(welterBrothers)
session.add(loai)
session.add(subscribe1)
session.add(post)
session.add(forum_cmnt)
session.add(game_cmnt)
session.commit()