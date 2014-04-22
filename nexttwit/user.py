from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(20))
    
    def __init__(self, username, email, password):
        self.username = username;
        self.email = email
        self.password = password
        
    def __repr__(self):
        return '<User %r %r %r %r>' % (self.id, self.username, self.email, self.password)