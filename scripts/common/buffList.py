from damage import Damage

class Buff:
	def __init__(self,time,unit,creater):#creater为unit
		self.timeLeft=time
		self.unit=unit#状态依附者
		self.creater=creater#状态制造者
	def start(self):
		pass
	def update(self,time):
		pass
	def befDelete(self):
		pass
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
				if not traget == None and not traget.ownerid== self.creater.ownerid:
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
				if not traget == None and not traget.ownerid== self.creater.ownerid and not traget == self.unit:
					self.creater.causeDamage(traget.no,Damage.MAGIC_DAMAGE(),20)
					distant=(traget.circle.center-self.unit.circle.center).normalized
					traget.repel.begin(distant,0.2,None,None)
			else:
				break
		print("_______redetonate")
		self.timeLeft=time
class coma(Buff):
	@staticmethod
	def no():
		return 2
	def start(self):
		self.unit.canAttack=False
		self.unit.canSkill=False
		self.unit.canMove=False
	def update(self,time):
		self.timeLeft-=time
		if self.timeLeft <= 0:
			self.unit.canAttack=True
			self.unit.canSkill=True
			self.unit.canMove=True
			self.unit.deleteBuff(self)
class temporaryShield(Buff):
	num=1
	@staticmethod
	def no():
		return 3
	def befDamage(self,damage):
		if damage.num>self.num:
			damage.num-=self.num
		else:
			damage.num=0
		self.num-=damage.num
		if self.num<=0:
			self.unit.deleteBuff(self)
	def start(self):
		if(self.unit.f_beforeTakeDamage == None):
			self.unit.f_beforeTakeDamage=[]
		self.unit.f_beforeTakeDamage.append(self.befDamage)
	def befDelete(self):
		self.unit.f_beforeTakeDamage.remove(self.befDamage)