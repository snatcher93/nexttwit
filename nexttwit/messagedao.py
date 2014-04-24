from message import Message
from database import dao, Dao
from user import User
from followerdao import followerDao
from flask import g

class MessageDao(Dao):
    def save(self, message):
        dao.add(message)
        self.__commit__()

    def findOne(self, id):
        return dao.query(Message).filter_by(id=id).first()
    
    def findAll(self):
        return dao.query(Message).order_by(Message.pubDate.desc()).all()

    def findByAuthor(self, user):
        return dao.query(Message)   \
                    .filter_by(authorId=user.id)   \
                    .order_by(Message.pubDate.desc())   \
                    .all()

    def findByAuthors(self, followings):
        following_ids = [each.whom_id for each in followings]
        following_ids.append(g.user.id)
        return dao.query(Message) \
                    .filter(Message.authorId.in_(following_ids))  \
                    .order_by(Message.pubDate.desc()) \
                    .all()

messageDao = MessageDao()        
