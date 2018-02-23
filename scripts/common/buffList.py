from damage import Damage

class Buff:
	def __init__(self,time,unit,creater):#creater为unit
		self.timeLeft=time
		self.unit=unit#状态依附者
		self.creater=creater#状态制造者
class burn(Buff):
	actionTime=1;
	@staticmethod
	def no():
		return 0
	def update(self,time):
		self.timeLeft-=time
		self.actionTime-=time
		if self.actionTime<=0:
			self.creater.causeDamage(self.unit.no,Damage.MAGIC_DAMAGE(),3)
			self.actionTime=1
		if self.timeLeft<=0:
			self.unit.deleteBuff(self)