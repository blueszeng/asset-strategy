import KBEngine
import Math
from ColliedSpace import *
from KBEDebug import *
from AI import AI
from AI import Event
from skilllist import skillList
from skill import Skill
from damage import Damage
import skillNumberList
import buffList
import trapList

unit_radiu=2
default_debug=[Vector2(5.0,5.0),Vector2(5.0,-5.0),Vector2(-5.0,5.0)]#用于除错阶段

class Repel:
	def __init__(self,unit):
		self.speed=[0,0]
		self.timeLeft=0
		self.unit=unit
		self.LastCallBack=None#onHit使用,用来remove
		self.onTheEnd=None
	def begin(self,arraw,time,onHit,onTheEnd):
		self.speed=[arraw.x/time,arraw.y/time]
		self.timeLeft=time
		if not self.LastCallBack == None:
			self.unit.circle.f_onColliedIn.remove(self.LastCallBack)
			self.LastCallBack=None
		if not onHit == None:
			self.unit.circle.f_onColliedIn.append(onHit)
			self.LastCallBack=onHit
		if not self.onTheEnd == None:
			self.onTheEnd()
		self.onTheEnd=onTheEnd
		self.unit.events.append(Event(self.unit.manager.beRepel,[arraw,time]))#arraw是Vector2
	def stop(self,doEnd=False):
		self.self.timeLeft=-1
		if not self.LastCallBack == None:
			unit.circle.f_onColliedIn.remove(self.LastCallBack)
			self.LastCallBack=None
		if doEnd and not onTheEnd==None:
			self.onTheEnd()
		self.onTheEnd=None
	def update(self,time):
		self.timeLeft-=time
		DEBUG_MSG("in repel timeLeft:{0}".format(self.timeLeft))
		if round(self.timeLeft,4) >= 0:#取4位整数
			self.unit.circle.center.x+=self.speed[0]*time
			self.unit.circle.center.y+=self.speed[1]*time
		else:
			if not self.onTheEnd==None:
				self.onTheEnd()
				self.onTheEnd=None
			if not self.LastCallBack == None:
				self.unit.circle.f_onColliedIn.remove(self.LastCallBack)
				self.LastCallBack=None
class time_resign:
	def __init__(self,time,function,arg):
		self.timeLeft=time
		self.function=function
		self.arg=arg
	def update(self,time):
		self.timeLeft-=time
		if self.timeLeft<=0:
			self.function(self.arg)
			return True #ture代表已经呼叫了function可以删除了
		else:
			return False
class arrow_resign:
	def __init__(self,speed,traget,oriPos,function,arg):
		self.speed=speed
		self.function=function
		self.arg=arg
		self.traget=traget
		self.position=Vector2(oriPos.x,oriPos.y)
	def update(self,time):
		tragetPos= self.traget.center
		if Vector2.distantBetween(self.position,tragetPos)-self.traget.radiu <= self.speed*time:#
			self.function(self.arg)
			return True
		else:
			self.position.x+=((tragetPos-self.position).normalized).x*self.speed*time
			self.position.y+=((tragetPos-self.position).normalized).y*self.speed*time
			return False
class unit:#单位物件包扩圆+转向+属性+事件
	@property
	def STAND_SPEED(self):
		return unit_radiu
	def __init__(self,circle,no,manager,ownerid):
		self.circle=circle
		self.no=no
		self.manager=manager
		self.ownerid=ownerid
		#DEBUG_MSG("in unit ownerid is:{0} so owner is".format(ownerid,KBEngine.entities[ownerid]))
		self._direct=Vector2(0,1)
		self._moving=False
		self.events=[]
		self.skills=[]
		self.buffs={}#用buff的no作为索引值的字典,添加buff和消除buff都只传buff的no这样做的坏处是一个角色身上同一种的buff只会有一个
		#註冊的觸發方法
		self.disabledBuffNo=[]#用于清除buff,因为在回圈中del会报长度改变错误
		self.f_beforeBeenSkill=None
		self.f_afterBeenSkill=None
		self.f_beforeTakeDamage=None
		self.f_afterTakeDamage=None
		self.f_beforeCauseDamage=None
		self.f_afterCauseDamage=None
		self.f_beforeSkill=None
		self.f_afterSkill=None
		self.f_beforeHealing=None
		self.f_afterHealing=None
		self.f_beforeBeenHealing=None
		self.f_afterBeenHealing=None
		self.f_beforeDied=None
		self.f_afterDied=None
		self.f_beforeKill=None
		self.f_afterKill=None
		
		self.LastSortList=None
		#属性变量
		self._speed=self.STAND_SPEED
		self._hp=100
		self._power=0
		self._canAttack=1#可否攻击
		self._canSkill=1#可否使用主动技能
		self._canMove=1
		self.repel=Repel(self)#被强迫的位移
		self.diedAlready=False
		#self.repel=None
	def singledele(self,kind,trigger):
			if kind==Skill.BEFORE_BEEN_SKILL():
				if self.f_beforeBeenSkill==None:
					self.f_beforeBeenSkill=[]
				self.f_beforeBeenSkill.append(trigger)
			elif kind==Skill.AFTER_BEEN_SKILL():
				if self.f_afterBeenSkill==None:
					self.f_afterBeenSkill=[]
				self.f_afterBeenSkill.append(trigger)
			elif kind==Skill.BEFORE_TAKE_DAMAGE():
				if self.f_beforeTakeDamage==None:
					self.f_beforeTakeDamage=[]
				self.f_beforeTakeDamage.append(trigger)
			elif kind==Skill.AFTER_TAKE_DAMAGE():
				if self.f_afterTakeDamage==None:
					self.f_afterTakeDamage=[]
				self.f_afterTakeDamage.append(trigger)
			elif kind==Skill.BEFORE_CAUSE_DAMAGE():
				if self.f_beforeCauseDamage==None:
					self.f_beforeCauseDamage=[]
				self.f_beforeCauseDamage.append(trigger)
			elif kind==Skill.AFTER_CAUSE_DAMAGE():
				if self.f_afterCauseDamage==None:
					self.f_afterCauseDamage=[]
				self.f_afterCauseDamage.append(trigger)
			elif kind==Skill.BEFORE_SKILL():
				if self.f_beforeSkill==None:
					self.f_beforeSkill=[]
				self.f_beforeSkill.append(trigger)
			elif kind==Skill.AFTER_SKILL():
				if self.f_afterSkill==None:
					self.f_afterSkill=[]
				self.f_afterSkill.append(trigger)
			elif kind==Skill.BRFORE_HEAL():
				if self.f_beforeHealing==None:
					self.f_beforeHealing=[]
				self.f_beforeHealing.append(trigger)
			elif kind==Skill.AFTER_HEAL():
				if self.f_afterHealing==None:
					self.f_afterHealing=[]
				self.f_afterHealing.append(trigger)
			elif kind==Skill.BRFORE_BEEN_HEAL():
				if self.f_beforeBeenHealing==None:
					self.f_beforeBeenHealing=[]
				self.f_beforeBeenHealing.append(trigger)
			elif kind==Skill.AFTER_BEEN_HEAL():
				if self.f_afterBeenHealing==None:
					self.f_afterBeenHealing=[]
				self.f_afterBeenHealing.append(trigger)
			elif kind==Skill.BEFORE_KILL():
				if self.f_beforeKill==None:
					self.f_beforeKill=[]
				self.f_beforeKill.append(trigger)
			elif kind==Skill.AFTER_KILL():
				if self.f_afterKill==None:
					self.f_afterKill=[]
				self.f_afterKill.append(trigger)
			elif kind==Skill.BEORE_DIED():
				if self.f_beforeDied==None:
					self.f_beforeDied=[]
				self.f_beforeDied.append(trigger)
			elif kind==Skill.AFTER_DIED():
				if self.f_afterDied==None:
					self.f_afterDied=[]
				self.f_afterDied.append(trigger)
	def initSkill(self,sList):
		for i in range(0,len(sList)):
			nowSkill=skillList[sList[i]](self.circle.radiu,self,i)
			DEBUG_MSG("on initskill {0}".format(i))
			#主動技能不註冊
			#註冊觸發方法
			if type(nowSkill.kind)==list:
				for i in range(0,len(nowSkill.kind)):#多重响应技能需要一个kind列表和一个trigger列表
					self.singledele(nowSkill.kind[i],nowSkill.triggers[i])	
			else:
				self.singledele(nowSkill.kind,nowSkill.trigger)
			self.skills.append(nowSkill)
	def initProperty(self,armor,armor_kind,hp,range=AI.NEAR_RANGE(unit_radiu)):
		self.armor=armor
		self._hp=hp
		self.armor_kind=armor_kind
		self.AI=AI(self,range)
	def update(self,manager):
		self.LastSortList=manager.space.getSortedCircleList(self.circle.center)
		'''templist=[]
		for pair in self.LastSortList:
			templist.append(pair.key.id)
		print("lastSortList be bulid {0}".format(templist))'''
		if not self.AI == None:#更新AI
			#print("no{0} AI update".format(self.no))
			self.AI.update(manager)
		if not self.repel == None:#更新repel
			self.repel.update(self.manager.cycle)
		for buff in self.buffs.values():
			buff.update(self.manager.cycle)
		#清理这一帧失效的buff
		for no in self.disabledBuffNo:
			del	self.buffs[no]
		self.disabledBuffNo=[]
	@property
	def direct(self):
		return self._direct
	@direct.setter 
	def direct(self,speed):
		if not speed[0]==self._direct.x or not speed[1]==self._direct.y:
			self._direct=Vector2(speed[0],speed[1])
			self.events.append(Event(self.manager.setDirect,speed))
	
	@property
	def moving(self):
		return self._moving
	@moving.setter 
	def moving(self,mov):
		if not mov==self._moving:
			self._moving=mov
			self.events.append(Event(self.manager.setMoving,mov))
	@property
	def speed(self):
		return self._speed
	@speed.setter 
	def speed(self,sp):
		self._speed=sp
		self.manager.setSpeed(self.no,sp)
	@property
	def hp(self):
		return self._hp
	@hp.setter 
	def hp(self,sp):
		print("no{0} hp {1}->{2}".format(self.no,self._hp,sp))
		self._hp=sp
	@property
	def canAttack(self):
		return self._canAttack>0
	@canAttack.setter
	def canAttack(self,TF):
		if TF:
			self._canAttack+=1
		else:
			self._canAttack-=1
	@property
	def canSkill(self):
		return self._canSkill>0
	@canSkill.setter
	def canSkill(self,TF):
		if TF:
			self._canSkill+=1
		else:
			self._canSkill-=1
	@property
	def canMove(self):
		return self._canMove>0
	@canMove.setter
	def canMove(self,TF):
		if TF:
			self._canMove+=1
		else:
			self._canMove-=1
		self.events.append(Event(self.manager.setcanMove,self.canMove))
	@property
	def power(self):
		return self._power
	@power.setter
	def power(self,p):
		self._power=p
	
	def SkillTo(self,skill,tragetNo):
		if type(tragetNo)==list:
			for no in tragetNo:
				traget=self.manager.getUnit(no)
				arg=[skill,traget]
				if self.f_beforeSkill:
					for s in self.f_beforeSkill:
							s(arg)
				if self.f_beforeBeenSkill:
					for s in traget.f_beforeBeenSkill:
							s(arg)
		else:
			traget=self.manager.getUnit(tragetNo)
			arg=[skill,traget]
			if self.f_beforeSkill:
				for s in self.f_beforeSkill:
						s(arg)
			if self.f_beforeBeenSkill:
				for s in traget.f_beforeBeenSkill:
						s(arg)
		self.events.append(Event(self.manager.useSkill,[skill.index,tragetNo]))
	def AfterSkillTo(self,skill,tragetNo):
		traget=self.manager.getUnit(tragetNo)
		arg=[skill,traget]
		if not self.f_afterSkill==None:
			for s in self.f_afterSkill:
				s(arg)
		if not self.f_afterBeenSkill==None:
			for s in traget.f_afterBeenSkill:
				s(arg)
	def takeDamage(self,damage):
		if not self.f_beforeTakeDamage == None:
			for function in self.f_beforeTakeDamage:
				function(damage)
		if damage.exist:
			#DEBUG_MSG("in bef takeDamage hp is{0}".format(self.hp))
			self.hp-=damage.num
			#DEBUG_MSG("in aft takeDamage hp is{0}".format(self.hp))
		arg=[damage,self]
		if not self.diedAlready:#如果角色还没死亡
			if self.hp<0:#这个判断是因为某些技能能让角色脱离死亡,通过改hp的方式
				if not self.f_beforeDied==None:
					for funcion in self.f_beforeDied:
						funcion(arg)
			if self.hp<0:
				if not damage.damager.f_beforeKill==None:
					for funcion in damage.damager.f_beforeKill:
						funcion(arg)
			self.events.append(Event(self.manager.takeDamage,damage.num))
			if self.hp<0:
				self.diedAlready=True
				self.manager.space.delCircle(self.circle)
				self.events.append(Event(self.manager.KillUnit,self))
				self.events.append(Event(self.manager.died,damage.damager.no))
				#刪除存在過的痕跡,以免有些技能用getUnit拿到NoneType
				for u in self.manager.units:
					if not u.AI == None and u.AI.traget==self.circle:
						u.AI.traget=None
					for index in range(0,len(u.LastSortList)):
						print("in died remove sortlist unit is:{0}".format(u.no))
						if u.LastSortList[index].key.id == self.no:
							print("remove no{0}".format(self.no))
							del u.LastSortList[index]
							break
				if not self.f_afterDied==None:
					for funcion in self.f_afterDied:
						funcion(arg)
				if not damage.damager.f_afterKill==None:
					for funcion in damage.damager.f_afterKill:
						funcion(arg)
		if not self.f_afterTakeDamage == None:
			for function in self.f_afterTakeDamage:
				function(damage)
	def beHealing(self,healpoint):
		if not self.f_beforeBeenHealing == None:
			for function in self.f_beforeBeenHealing:
				function(healpoint)
		if healpoint.exist:
			self.hp-=healpoint.num
			self.events.append(Event(self.manager.beTreat,healpoint.num))
		if not self.f_afterBeenHealing == None:
			for function in self.f_afterBeenHealing:
				function(healpoint)
		
	def healingTo(self,tragetNo,num):
		#print("heal tragetNo is {0}".format(tragetNo))
		traget=self.manager.getUnit(tragetNo)
		healpoint=Damage(2,num,self)
		if not self.f_beforeHealing == None:
			for function in self.f_beforeHealing:
				function([traget,healpoint])
		traget.beHealing(healpoint)
		if not self.f_afterHealing == None:
			for function in self.f_afterHealing:
				function([traget,healpoint])
	def causeDamage(self,tragetNo,kind,num):
		#print("cause tragetNo is {0}".format(tragetNo))
		traget=self.manager.getUnit(tragetNo)
		if not traget == None:
			newd=Damage(kind,int(num),self)
			Damage.calAdditon(newd,self.power)
			Damage.calVulnerable(newd,traget.armor_kind)
			Damage.calReduce(newd,traget.armor)
			if not self.f_beforeCauseDamage == None:
				for function in self.f_beforeCauseDamage:
					function([traget,newd])
			traget.takeDamage(newd)
			if not self.f_afterCauseDamage == None:
				for function in self.f_afterCauseDamage:
					function([traget,newd])
	def addBuff(self,buffClass,time,creater):
		#other.buffs[buffList.burn.no()]=buffList.burn(5,other,self.unit)#添加一个新的燃烧buff
		buff=buffClass(time,self,creater)
		buff.start()
		self.buffs[buff.no()]=buff
		self.events.append(Event(self.manager.addBuff,buff.no()))
	def deleteBuff(self,buff):
		self.disabledBuffNo.append(buff.no())
		self.events.append(Event(self.manager.deleteBuff,buff.no()))
class roundCount:
	def __init__(self,nolist,round):
		self.roleNoList=nolist
		self.roundCount=0
		self.Max=round
		self.roundStart=[]
		self.roundEnd=[]
		self.beginTrap=[]
		self.totalEnd=[]
	def nextround(self):
		if not self.roundCount==0:
			index=self.roundCount%len(nolist)
			self.roundEnd(nolist[index])
		self.roundCount+=1
		if(self.roundCount>Max):
			self.totalEnd()
		else:
			index=self.roundCount%len(nolist)
			self.roundStart(nolist[index])
class WarField(KBEngine.Entity):
	def shiftCallBack(self,no,x,y):
		if not no in self.shiftRecord.keys():#這個防呆是因為出現過,因為center改變的反射導致space 的record改變,同一個circle被計算shift兩次
			self.shiftRecord[no]=[x,y]
		#DEBUG_MSG("in shift record no{1} shift is {0}".format(self.shiftRecord[no],no))
	def gameStart(self):
		self.run=True
		for unit in self.units:
			for skill in unit.skills:
				skill.inBegin()
		self.rCounter=None
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("WarField Cell done")
		self.space=XYCollied(2,4,-4*unit_radiu,-8*unit_radiu,4*unit_radiu,4*unit_radiu,self.shiftCallBack)#圆半径是10,格子宽度是两个圆也就是10*2 *2
		#设置round
		self.units=[]
		self.traps=[]#记录陷阱物件
		self.cemetery=[]#存放死去的单位
		self.resigns=[]#延迟触发记录
		self.playerIds=[]
		self.cycle=0.1#更新周期
		self.timerId=self.addTimer(0.1,0.1,0)
		self.shiftRecord={}
		self.frame_num=1#用来记录第几帧
		self.trapCount=0#用来产生陷阱的no
		self.run=False
		#除错代码
		'''i=0
		for pos in default_debug:
			self.newUnit(0,pos.x,pos.y,47+i)
			i+=1
		for unit in self.units:
			print("no{0} circle in space? ans:{1}".format(unit.no,unit.circle in self.space.circles.getNode(unit.circle.center.x,unit.circle.center.y).subNode))'''

	def getUnit(self,no):
		for unit in self.units:
			if unit.no==no:
				return unit
		return None
	def onTimer( self, id, userArg ):
		if self.run:
			#先做物理判定
			self.space.Collied()
			for unit in self.units:
				if not unit.circle in self.space.circles.getNode(unit.circle.center.x,unit.circle.center.y).subNode:
					print("!!!!!!!!!!!!error:unit{0} not in its node!!!!!!!!!!!".format(unit.no))
					for node in self.space.record:
						for c in node.subNode:
							if c == unit.circle:
								print("unit{0} in node({1},{2})".format(unit.no,node.getIndexX(self.space.circles),node.getIndexY(self.space.circles)))
								realnode=self.space.circles.getNode(unit.circle.center.x,unit.circle.center.y)
								print("while node is ({0},{1})".format(realnode.getIndexX(self.space.circles),realnode.getIndexY(self.space.circles)))
								print("unit pos ({0},{1})".format(unit.circle.center.x,unit.circle.center.y))
			print("collied end")
			#處理之前註冊的record
			for record in self.resigns:
				if record.update(self.cycle):
					self.resigns.remove(record)
			print("record end")
			#主動技能觸發
			for unit in self.units:
				for s in unit.skills:
					s.onTime(self.cycle)
				for s in unit.skills:
					if s.kind == Skill.ACTIVE():
						s.trigger(None)#canUse自己在方法裏面判斷
			for unit in self.units:#主逻辑回圈,更新单位的AI,将单位速度和位移传给客户端
				#DEBUG_MSG("unit{0} center is {1}".format(unit.no,unit.circle.center))
				self.turnNo(unit.no)#该单位的更新周期开始
				unit.update(self)#在这里有创建sortlist->更新AI
				#更新技能
				print("no{0} events has {1} event".format(unit.no,len(unit.events)))
				for event in unit.events:
					print(event.funcion)
					event.funcion(event.arg)
				unit.events.clear()
				#发送挤压的击退值
				#DEBUG_MSG("circle id{0} lastShiftx:{1} lastShifty:{2} center{3}".format(unit.circle.id,unit.circle.lastShiftx,unit.circle.lastShifty,str(unit.circle.center)))
				shift=self.shiftRecord[unit.circle.id]
				#
				if not shift[0]==0 or not shift[1]==0:
					self.setShift(shift)
					print("in shift {0}".format(shift))
					#print("its no is{0}".format(unit.circle.id))
				del self.shiftRecord[unit.circle.id]
				#再做速度移动
					#DEBUG_MSG("norm:({2},{3}) speed:({0},{1})".format(norm.x*unit.speed*self.cycle,norm.y*unit.speed*self.cycle,norm.x,norm.y))
				#debug代码
				#DEBUG_MSG("position after is {0}".format(unit.circle.center))
				#再做AI
			for unit in self.units:
				if unit.moving and unit.canMove:
					norm=unit.direct.normalized
					#debug代码
					#DEBUG_MSG(">>in final moving:{0} canMove{1}".format(unit.moving,unit.canMove))
					#DEBUG_MSG("no{0}".format(unit.no))
					#DEBUG_MSG("norm is "+str(unit.direct.normalized))
					#------------------------
					unit.circle.center.x+=norm.x*unit.speed*self.cycle
					unit.circle.center.y+=norm.y*unit.speed*self.cycle
				#DEBUG_MSG("no{0} final position:{1}".format(unit.no,unit.circle.center))
			self.updateEnd()
	def newUnit(self,rolekind,posx,posy,ownerid):
		circle=self.space.addCircle(Vector2(posx,posy),unit_radiu)
		unitNo=circle.id
		newone=unit(circle,unitNo,self,ownerid)
		DEBUG_MSG("**new unit rolekind{0} list{1}".format(rolekind,skillNumberList.list[rolekind]))
		p=skillNumberList.propertys[rolekind]
		newone.initProperty(p[0],p[1],p[2],skillNumberList.ranges[rolekind])
		newone.initSkill(skillNumberList.list[rolekind])
		self.units.append(newone)
		for pid in self.playerIds:
			DEBUG_MSG("pid is {0}".format(pid))
			KBEngine.entities[pid].p_addnewUnit(unitNo,rolekind,skillNumberList.list[rolekind],posx,posy,ownerid)
			#KBEngine.entities[pid].client.int64({"list":[90,99]})
	def KillUnit(self,unit):
		self.units.remove(unit)
	def createTrap(self,trapNo,posx,posy,ownerId):
		self.traps.append(trapList.trapList[trapNo](self,self.trapCount,ownerId))
		trapCount+=1
		if not self.rCounter==None:
			self.rCounter.nextround()
	def delTrap(self,trapNo):
		for trap in self.traps:
			if trap.no == trapNo:
				self.traps.remove(trap)
				trap.befDestory()
				return

	def playerSignIn(self,pid):
		self.playerIds.append(pid)
		self.rCounter=roundCount([self.playerIds[0],4747],5)
		self.rCounter.totalEnd.append(self.gameStart)
		
		rolekind=0
		#self.run=True
	def playerSignOut(self,pid):
		self.playerIds.remove(pid)
		if len(self.playerIds)<=0:
			self.destroy()
	def setSpeed(self,new):
		DEBUG_MSG("setSpeed")
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setSpeed(new)
	def setDirect(self,new):
		DEBUG_MSG("setDirect {0}".format(new))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setDirect(new)
	def setShift(self,new):
		#DEBUG_MSG("setShift {0}".format(new))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setShift(new)
	def setMoving(self,new):
		DEBUG_MSG("setMoving")
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setMoving(new)
	def turnNo(self,no):
		DEBUG_MSG("turnNo{0}=============================================".format(no))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_turnNo(no)
	def useSkill(self,list):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_useSkill(list[0],list[1])
	def takeDamage(self,num):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_takeDamage(num)
	def beTreat(self,num):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_beTreat(num)
	def beRepel(self,list):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_beRepel(list[0],list[1])
	def addBuff(self,buffNo):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_addBuff(buffNo)
	def deleteBuff(self,buffNo):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_deleteBuff(buffNo)
	def createEffection(self,arg):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_createEffection(arg[0],arg[1])
	def updateEnd(self):
		DEBUG_MSG("update {0} end-----------------------------------------".format(self.frame_num))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_updateEnd(self.frame_num)
		self.frame_num+=1
	def died(self,useless):
		DEBUG_MSG("KKKKKKKKKKKKKKKKKKKK manager:died be call")
		for pid in self.playerIds:
			KBEngine.entities[pid].p_died()
	def setcanMove(self,TF):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setcanMove(TF)
	def signUpTime(self,time,function,arg):
		self.resigns.append(time_resign(time,function,arg))
	def signUpArrow(self,speed,traget,oriPos,function,arg):
		self.resigns.append(arrow_resign(speed,traget,oriPos,function,arg))