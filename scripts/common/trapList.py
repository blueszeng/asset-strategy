#that`s a trap
class Trap:
	def __init__(self,manager,no,ownerId):
		self.manager=manager
		self.no=no
		self.ownerId=ownerId
	def update(self,time):
		pass
	def befDestory(self):
		pass
	def delSelf(self):
		self.manager.delTrap(self.no)
class seizaSeat(Trap):
	def __init__(self,manager,no,ownerId):
		super().__init__(manager,no,ownerId)
	def roundBegin(self,ownerId):
		if self.ownerId==ownerId:#轮到自己的回合
			self.delSelf()
	def gameStart(self):
			self.delSelf()
#正文------------------------------------------
trapList=[seizaSeat]