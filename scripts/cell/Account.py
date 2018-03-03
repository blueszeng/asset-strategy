import KBEngine
import Math
from KBEDebug import *
class Account(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("account create cell success!")
		KBEngine.entities[self.WarFieldId].playerSignIn(self.id)
		KBEngine.entities[self.WarFieldId].newUnit(0,0.0,0.0,self.id)
	def p_addnewUnit(self,unitNo,rolekind,skillList,posx,posy,oid):
		DEBUG_MSG("in p_addnewUnit unitNo is {0} list{1}".format(unitNo,skillList))
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
		DEBUG_MSG("rolekind{0} skillList{1}".format(rolekind,skillList))
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
		node=self.Slave.manager.space.circles.getNode(self.Slave.circle.center.x,self.Slave.circle.center.y)
		print("slave in node ({0},{1}) in?{2}".format(node.getIndexX(self.Slave.manager.space.circles),node.getIndexY(self.Slave.manager.space.circles),self.Slave.circle in node.subNode))
	def p_takeDamage(self,num):
		self.client.takeDamage(num)
	def p_useSkill(self,skillindex,tragetNo):
		self.client.useSkill(skillindex,tragetNo)
	def p_beTreat(self,num):
		self.client.beTreat(num)
	def p_beRepel(self,arraw,time):#arraw是Vector2
		self.client.beRepel((arraw.x,arraw.y),time)
	def p_addBuff(self,buffno):
		self.client.addBuff(buffno)
	def p_deleteBuff(self,buffno):
		self.client.delBuff(buffno)
	def p_died(self):
		self.client.died()