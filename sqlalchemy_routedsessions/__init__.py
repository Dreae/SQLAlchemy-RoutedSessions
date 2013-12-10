from sqlalchemy.orm import Session
import random

class RoutedSession(Session):
	def get_bind(self, mapper=None, clause=None):
		if self._flushing:
			engine = api().get_engine(True)
			return engine
		else:
			engine = api().get_engine()
			return engine
			
class RoutedSessionMaker(object):
	Mode_RoundRobin = 1 << 0
	Mode_Random = 1 << 1
	
	def __init__(self, balancing_mode=Mode_RoundRobin, engines=[]):
		self._mode = balancing_mode
		self._engines = engines
		self.last_master = 0
		self.last_slave = 0
		
	def add_engine(self, engine):
		self._engines.append(engine)
		
	def get_engine(self, flushing=False):
		if flushing:
			if self._mode == self.Mode_RoundRobin:
				masters = [engine._engine for engine in self._engines if engine._type == RoutedEngine.Engine_Master]
				if self.last_master + 1 >= len(masters):
					self.last_master = 0
					return masters[self.last_master]
				else:
					self.last_master += 1
					return masters[self.last_master]
			elif self._mode == self.Mode_Random:
				return random.choice([engine._engine for engine in self._engines if engine._type == RoutedEngine.Engine_Master])
		else:
			if self._mode == self.Mode_RoundRobin:
				slaves = [engine._engine for engine in self._engines if engine._type == RoutedEngine.Engine_Slave]
				if self.last_slave + 1 >= len(slaves):
					self.last_slave = 0
					return slaves[self.last_slave]
				else:
					self.last_slave += 1
					return slaves[self.last_slave]
			elif self._mode == self.Mode_Random:
				return random.choice([engine._engine for engine in self._engines if engine._type == RoutedEngine.Engine_Slave])

class RoutedEngine(object):
	Engine_Slave = 1 << 0
	Engine_Master = 1 << 1
	
	def __init__(self, type=Engine_Slave, engine=None):
		self._type = type
		self._engine = engine
	
	def __repr__(self):
		return 'Master: ' if self.type == Engine_Master else 'Slave: ' + self._engine

__sessionmaker = RoutedSessionMaker()

def Configure(mode=RoutedSessionMaker.Mode_RoundRobin, engines=[]):
	global __sessionmaker
	__sessionmaker = RoutedSessionMaker(balancing_mode=mode, engines=engines)

def api():
	global __sessionmaker
	return __sessionmaker