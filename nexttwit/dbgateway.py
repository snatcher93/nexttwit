from messagedao import messageDao
from userdao import userDao
from followerdao import followerDao
 
class DBGateway:
    def insertMessage(self, message):
        messageDao.save(message)
        
    def findMessages(self):
        return messageDao.findAll()

    def findUser(self, userid):
        return userDao.findByUserId(userid)

    def saveFollower(self, follower):
        followerDao.save(follower)
    
database = DBGateway()