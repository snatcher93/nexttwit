from user import User
from database import dao, Dao

class UserDao(Dao):
    def save(self, user):
        dao.add(user)
        self.__commit__()

    def findOne(self, id):
        return dao.query(User). \
                filter_by(id=id). \
                first()

    def findByName(self, name):
        return dao.query(User). \
                filter_by(username=name). \
                first()

    def findAll(self):
        return dao.query(User).all()
    
userDao = UserDao()