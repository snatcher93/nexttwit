from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from user import User
from database import Base

class Follower(Base):
    __tablename__ = "followers"
    
    id = Column(Integer, primary_key = True)
    who_id = Column(Integer, ForeignKey('users.id'))
    whom_id = Column(Integer, ForeignKey('users.id'))
    
    who = relationship("User", foreign_keys=[who_id])
    whom = relationship("User", foreign_keys=[whom_id])
    
    def __init__(self, who, whom):
        self.who_id = who.id;
        self.whom_id = whom.id;
        
    def __repr__(self):
        return '<Follower %r %r>' % (self.who_id, self.whom_id)