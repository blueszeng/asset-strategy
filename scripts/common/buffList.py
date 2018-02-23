class Buff:
	def __init__(self,time,unit):
		self.timeLeft=time
		self.unit=unit
class burn(buff):
	def update(self,time):
		self.timeLeft-=time