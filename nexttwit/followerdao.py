from follower import Follower
from database import dao, Dao

class FollowerDao(Dao):
    def save(self, follower):
        dao.add(follower)
        dao.commit()
    
    def find(self, who_id, whom_id):
        return dao.query(Follower). \
                    filter_by(who_id=who_id, whom_id=whom_id). \
                    first()

    def findFollowings(self, who_id):
        return dao.query(Follower). \
                    filter_by(who_id=who_id). \
                    all()
    
    def delete(self, follower):
        dao.delete(follower)
        dao.commit()

followerDao = FollowerDao()