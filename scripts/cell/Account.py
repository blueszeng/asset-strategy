import KBEngine
import Math
from KBEDebug import *
class Account(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("account create cell success!")
		KBEngine.entities[self.WarFieldId].playerSignIn(self.id)
		KBEngine.entities[self.WarFieldId].newUnit(0,[],0.0,0.0,self.id)
	def p_addnewUnit(self,unitNo,rolekind,skillList,posx,posy,oid):
		DEBUG_MSG("in p_addnewUnit unitNo is {0}".format(unitNo))
		units=KBEngine.entities[self.WarFieldId].units
		for unit in units:
			if unit.no == unitNo:
				if unit.ownerid==self.id:
					self.Slave=unit
					#除错代码取消AI
					self.Slave.AI=None
					DEBUG_MSG('set Slave:{0}'.format(self.Slave))
					break
		DEBUG_MSG("addNewUnit position float({0},{1}) int({2},{3})".format(float(posx),float(posy),posx,posy))
		self.client.addNewUnit(unitNo,rolekind,{"list":skillList},float(posx),float(posy),oid)
	def move(self,expose,pos):
		center=self.Slave.circle.center
		self.Slave.direct=[pos[0]-center.x,pos[1]-center.y]
		self.Slave.moving=True
		#self.position=newpos
		#DEBUG_MSG("move control by is:{1}",format(self.controlledBy))
		#self.moveToPoint(newpos,1.0,0.1,dir,False,True)
	def onDestroy( self ):
		if not self.WarFieldId==-1:#有在房間中
			KBEngine.entities[self.WarFieldId].playerSignOut(self.id)
	def onMoveOver( self, controllerID, userData ):
		self.controlledBy=None
		DEBUG_MSG("move is over pos:{1}",format(self.position))
	def p_setDirect(self,new):
		self.client.setDirect((new[0],new[1]))
	def p_setMoving(self,new):
		self.client.setMoving(new)
	def p_setSpeed(self,new):
		self.client.setSpeed(new)
	def p_setShift(self,new):
		self.client.setShift((new[0],new[1]))
	def p_turnNo(self,no):#轮到第no号角色更新状态
		self.client.turnNo(no)
	def p_updateEnd(self,count):
		self.client.updateEnd(count)