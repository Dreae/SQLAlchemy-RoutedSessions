import sqlalchemy_routedsessions as routedsessions
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import shutil

Base = declarative_base()

class Model1(Base):
	__tablename__ = 'test_table'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	
	def __init__(self, name):
		self.name = name

if __name__ == '__main__':
	routedsessions.Configure(mode=routedsessions.RoutedSessionMaker.Mode_Random)
	routedsessions.api().add_engine(routedsessions.RoutedEngine(routedsessions.RoutedEngine.Engine_Master, create_engine("sqlite:///master.db")))
	routedsessions.api().add_engine(routedsessions.RoutedEngine(routedsessions.RoutedEngine.Engine_Slave, create_engine("sqlite:///slave1.db")))
	routedsessions.api().add_engine(routedsessions.RoutedEngine(routedsessions.RoutedEngine.Engine_Slave, create_engine("sqlite:///slave2.db")))
	routedsessions.api().add_engine(routedsessions.RoutedEngine(routedsessions.RoutedEngine.Engine_Slave, create_engine("sqlite:///slave3.db")))
	
	session = scoped_session(sessionmaker(class_=routedsessions.RoutedSession))
	Base.metadata.create_all(routedsessions.api().get_engine(True))
	
	session.add(Model1("Test1"))
	session.add(Model1("Test2"))
	session.add(Model1("Test3"))
	session.commit()
	
	shutil.copy("master.db", "slave1.db")
	shutil.copy("master.db", "slave2.db")
	shutil.copy("master.db", "slave3.db")
	
	session.query(Model1).all()
	session.query(Model1).all()
	session.query(Model1).all()
	session.query(Model1).all()
	session.query(Model1).all()