import KBEngine
from KBEDebug import *

class WarField(KBEngine.Base):
	mode=0#0为debug游戏模式
	startNum=1
	preLoadList=[]
	def __init__(self):
		KBEngine.Base.__init__(self)
		DEBUG_MSG("WarField Base done")
	def addPlayer(self,player):
		self.preLoadList.append(player)
		if len(self.preLoadList) >= self.startNum:
			print("in WarField addPlayer perloadlist{0} startNum{1}".format(self.preLoadList,self.startNum))
			self.cellData["playerNum"]=self.startNum
			self.cellData["mode"]=self.mode
			self.createInNewSpace(None)
	def onGetCell( self ):
		for aBase in self.preLoadList:
			print("in WarField get cell aBase id:{0}".format(aBase.id))
			aBase.state=2#account进入游戏中状态
			aBase.cellData["WarFieldId"]=self.id
			aBase.cellData["gameMode"]=self.mode
			aBase.createCellEntity(self.cell)
			#aBase.client.cellReady(self.mode)
		self.preLoadList.clear()
	def onLoseCell(self):
		self.destroy(False,False)

