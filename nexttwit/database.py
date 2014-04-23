from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DBManager:
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag) 
        DBManager.__session = \
            scoped_session(sessionmaker(autocommit=False, 
                                        autoflush=False, 
                                        bind=DBManager.__engine))

        global dao
        dao = DBManager.__session
    
    @staticmethod
    def init_db():
        from user import User
        from message import Message
        from follower import Follower
        Base.metadata.create_all(bind=DBManager.__engine)

class Dao:
    def __commit__(self):
        dao.commit()
        
dao = None  

def initializeDB(dbUrl, dbLogFlag):
    DBManager.init(dbUrl, dbLogFlag)    
    DBManager.init_db()

      
