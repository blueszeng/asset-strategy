import buffList
from damage import Damage

#that`s a trap
class Trap:
	def __init__(self,manager,no,ownerId,position):
		self.manager=manager
		self.no=no
		self.ownerId=ownerId
		self.center=position
	def update(self,time):
		pass
	def befDestory(self):
		pass
	def delSelf(self):
		self.manager.delTrap(self.no)
	def afterBeenCreate(self,rCounter):
		rCounter.nextround()
class default_sizeaSeat(Trap):
	def gameStart(self):
		self.delSelf()
	def __init__(self,manager,no,ownerId,position):
		super().__init__(manager,no,ownerId,position)
		if not manager.rCounter == None:
			manager.rCounter.totalEnd.append(self.gameStart)
class seizaSeat(Trap):
	def roundBegin(self,ownerId):
		if self.ownerId==ownerId:#轮到自己的回合
			self.delSelf()
	def gameStart(self):
			self.delSelf()
	def __init__(self,manager,no,ownerId,position):
		super().__init__(manager,no,ownerId,position)
		if not manager.rCounter == None:
			manager.rCounter.roundStart.append(self.roundBegin)
			manager.rCounter.totalEnd.append(self.gameStart)
class protectShield(Trap):
	radiu=1
	def update(self,time):
		inside= self.manager.space.castCircle(self.center,self.radiu)
		#print("!!!!!!in protectShield len is"+str(len(inside)))
		if len(inside)>0:#有目标
			traget= self.manager.getUnit(inside[0].key.id)
			traget.addBuff(buffList.temporaryShield,10,None)
			self.delSelf()
class explodeTrap(Trap):
	radiu=1
	exp_radiu=2
	timing=False
	time=0
	def update(self,time):
		if not self.timing:
			inside= self.manager.space.castRadiuCircle(self.center,self.radiu)
			if len(inside)>0:
				self.timing=True
				self.time=0.4
				self.manager.createEffection([19,(self.center.x,self.center.y)])
		if self.timing:
			self.time-=time
			if self.time<=0:
				tragets=self.manager.space.castCircle(self.center,self.exp_radiu)
				for pair in tragets:
					unit=self.manager.getUnit(pair.key.id)
					newd=Damage(Damage.REAL_DAMAGE(),20,None)
					unit.takeDamage(newd)
				self.delSelf()
class Trapper(Trap):
	radiu=1
	def update(self,time):
		inside= self.manager.space.castRadiuCircle(self.center,self.radiu)
#正文------------------------------------------
trapList=[seizaSeat,protectShield,default_sizeaSeat,explodeTrap]