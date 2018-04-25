# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Account(KBEngine.Proxy):
	def fieldOk(self,field):
		field.addPlayer(self)
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		DEBUG_MSG("account createCellEntity")
		self.state=0#0:空闲,; 1:匹配中; 2:游戏中
		#if  KBEngine.globalData.has_key["space"]:
		#	self.createCellEntity(KBEngine.globalData["space"].cell)
		#else:
		#	KBEngine.globalData["space"]=self.createInNewSpace()
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onEntitiesEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		#self.cellData["position"]=(0,0,0)
		#self.cellData["WarFieldId"]=KBEngine.globalData["one"].id#加入warField的id用于cell类别的呼叫方法
		DEBUG_MSG("global Hall is{0}".format(KBEngine.globalData["Hall"]))
		#self.createCellEntity(KBEngine.globalData["one"].cell)
		INFO_MSG("account[%i] entities enable. mailbox:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		if self.state==1:
			KBEngine.globalData["Hall"].removeWaiter(self)
		if not self.cell == None:
			self.destroyCellEntity()
	def onLoseCell(self):
		self.destroy()
	def onGetCell(self):
		pass
	def createSpace(self):
		self.space = pymunk.Space()
	def startDebugMode(self):
		KBEngine.createBaseAnywhere("WarField",{},self.fieldOk)
	def startMatching(self):
		KBEngine.globalData["Hall"].addToWaiterList(self)