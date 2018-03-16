import KBEngine
from KBEDebug import *

class WarField(KBEngine.Base):
	startNum=1
	preLoadList=[]
	def __init__(self):
		KBEngine.Base.__init__(self)
		DEBUG_MSG("WarField Base done")
	def addPlayer(self,player):
		self.preLoadList.append(player)
		if len(self.preLoadList) >= self.startNum:
			self.createInNewSpace(None)
	def onGetCell( self ): 
		for aBase in self.preLoadList:
			aBase.cellData["WarFieldId"]=self.id
			aBase.createCellEntity(self.cell)
		self.preLoadList.clear()
	def onLoseCell(self):
		self.destroy(False,False)

