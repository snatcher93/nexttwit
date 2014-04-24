from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base
from user import User
import time

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key = True)
    authorId = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)
    pubDate = Column(Integer)
    retwit = Column(Boolean)
    origin_author = Column(String) 
     
    author = relationship("User")
    
    def __init__(self, author, message, origin=None):
        self.authorId = author.id
        self.author = author
        self.pubDate = int(time.time())
        self.message = message 

        if origin is not None:
            self.retwit = True
            self.origin_author = origin.author.userid
        else:
            self.retwit = False
            
        
    def __repr__(self):
        return '<Message %r %r %r %r>' % (self.authorId, self.message, self.pubDate, self.origin_author)