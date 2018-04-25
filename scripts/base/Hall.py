import KBEngine
from KBEDebug import *

class Hall(KBEngine.Base):
	def onCreateFieldOK(self,entity):
		if not entity == None:
			entity.startNum=2
			entity.mode=1#1为连线游戏模式
			self.fieldPool.append(entity)
	def removeWaiter(self,account):
		self.waiterList.remove(account)
	def __init__(self):
		KBEngine.Base.__init__(self)
		self.fieldPool=[]
		self.waiterList=[]
		for i in range(0,self.idleRoomNum):
			KBEngine.createBaseAnywhere("WarField",{},self.onCreateFieldOK)
		
		self.addTimer(0.5,0.5,0)
	def addToWaiterList(self,account):
		self.waiterList.append(account)
		account.state=1
	def onTimer( self, timerHandle, userData ):
		if len(self.waiterList)<=0 or len(self.fieldPool)<=0:#如果没有人在等待或者没有空闲的房间
			return
		else:
			'''for i in range(0,int(len(self.waiterList)/2)):
				self.fieldPool[0].addPlayer(self.waiterList[2*i])
				self.fieldPool[0].addPlayer(self.waiterList[2*i+1])
				del self.fieldPool[0]'''
			while len(self.waiterList)>=2:#如果还有2个或以上的等待玩家的话
				self.fieldPool[0].addPlayer(self.waiterList[0])
				self.fieldPool[0].addPlayer(self.waiterList[1])
				self.waiterList=self.waiterList[2:]
				del self.fieldPool[0]
				if len(self.fieldPool)<=0:#如果已经没有空闲的房间
					return
		for i in range(0,self.idleRoomNum-len(self.fieldPool)):
			KBEngine.createBaseAnywhere("WarField",{},self.onCreateFieldOK)