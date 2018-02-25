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
class bombCounter(Buff):
	range=4
	@staticmethod
	def no():
		return 1
	def update(self,time):
		self.timeLeft-=time
		if self.timeLeft <= 0:
			self.detonate()
	def detonate(self):
		self.creater.causeDamage(self.unit.no,Damage.MAGIC_DAMAGE(),20)
		for pair in self.unit.LastSortList:
			if pair.value <= self.range +pair.key.radiu:
				traget= self.unit.manager.getUnit(pair.key.id)
				if not traget.ownerid== self.creater.ownerid:
					self.creater.causeDamage(traget.no,Damage.MAGIC_DAMAGE(),20)
					distant=(traget.circle.center-self.unit.circle.center).normalized
					traget.repel.begin(distant,0.2,None,None)
			else:
				break
		print("detonate_______")
		self.unit.deleteBuff(self)
	def redetonate(self,time):
		self.creater.causeDamage(self.unit.no,Damage.MAGIC_DAMAGE(),20)
		for pair in self.unit.LastSortList:
			if pair.value <= self.range +pair.key.radiu:
				traget= self.unit.manager.getUnit(pair.key.id)
				if not traget.ownerid== self.creater.ownerid and not traget == self.unit:
					self.creater.causeDamage(traget.no,Damage.MAGIC_DAMAGE(),20)
					distant=(traget.circle.center-self.unit.circle.center).normalized
					traget.repel.begin(distant,0.2,None,None)
			else:
				break
		print("_______redetonate")
		self.timeLeft=time