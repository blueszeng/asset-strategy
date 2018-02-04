import KBEngine
import Math
from ColliedSpace import *
from KBEDebug import *
from AI import AI
from AI import Event
from skilllist import skillList
from skill import skill
from damage import damage

unit_radiu=2
default_debug=[Vector2(2.0,2.0)]#,Vector2(2.0,-2.0),Vector2(-2.0,2.0)]#用于除错阶段
class time_resign:
	def __init__(self,time,fuction,arg):
		self.timeLeft=time
		self.fuction=fuction
		self.arg=arg
	def update(time):
		self.timeLeft-=time
		if self.timeLeft<=0:
			self.fuction(arg)
			return True #ture代表已经呼叫了fuction可以删除了
		else:
			return False
class arrow_resign:
	def __init__(self,speed,traget,oriPos,function,arg):
		self.speed=speed
		self.fuction=fuction
		self.arg=arg
		self.traget=traget
		self.position=oriPos
	def update(time):
		tragetPos= traget.circle.center
		distant=Vector2.betw
		if Vector2.distantBetween(self.position,tragetPos)-traget.circle.radiu <= self.speed*time:#
			self.function(arg)
			return True
		else:
			self.position+=(tragetPos-self.position).normalized*self.speed*time

class unit:#单位物件包扩圆+转向+属性
	@property
	def STAND_SPEED(self):
		return unit_radiu

	def __init__(self,circle,no,manager,ownerid):
		self.circle=circle
		self.no=no
		self.manager=manager
		self.ownerid=ownerid
		#DEBUG_MSG("in unit ownerid is:{0} so owner is".format(ownerid,KBEngine.entities[ownerid]))
		self.AI=AI(self,AI.NEAR_RANGE(unit_radiu))
		self._direct=Vector2(0,0)
		self._moving=False
		self.events=[]
		self.skills=[]
		#註冊的觸發方法
		self.f_beforeBeenSkill=[]
		self.f_afterBeenSkill=[]
		self.f_beforeTakeDamage=[]
		self.f_afterTakeDamage=[]
		self.f_beforeCauseDamage=[]
		self.f_afterCauseDamage=[]
		self.f_beforeSkill=[]
		self.f_afterSkill=[]
		#属性变量
		self._speed=self.STAND_SPEED
		self._hp=100
	def initSkill(self,list):
		for i in range(0,len(list)):
			nowSkill=skillList[list[i]](self.circle.radiu,self,i)
			#主動技能不註冊
			#註冊觸發方法
			if nowSkill.kind==skill.BEFORE_BEEN_ATTACK():
				self.f_beforeBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==skill.AFTER_BEEN_ATTACK():
				self.f_afterBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==skill.BEFORE_TAKE_DAMAGE():
				self.f_beforeBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==skill.AFTER_TAKE_DAMAGE():
				self.f_afterBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==skill.AFTER_TAKE_DAMAGE():
				self.f_afterBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==skill.BEFORE_SKILL():
				self.f_beforeSkill.append(nowSkill.trigger)
			elif nowSkill.kind==skill.AFTER_SKILL():
				self.f_afterSkill.append(nowSkill.trigger)
	def initProperty(self,power,intel,armor,sp_armor,physique):
		self.power=power
		self.intel=intel
		self.armor=armor
		self.sp_armor=sp_armor
		self.physique=physique
	def update(self,space):
		if not self.AI == None:
			print("no{0} AI update".format(self.no))
			self.AI.update(space)
	@property
	def direct(self):
		return self._direct
	@direct.setter 
	def direct(self,speed):
		if not speed[0]==self._direct.x or not speed[1]==self._direct.y:
			self._direct=Vector2(speed[0],speed[1])
			self.manager.setDirect(speed)
	
	@property
	def moving(self):
		return self._moving
	@moving.setter 
	def moving(self,mov):
		if not mov==self._moving:
			self._moving=mov
			self.manager.setMoving(mov)
	@property
	def speed(self):
		return self._speed
	@speed.setter 
	def speed(self,sp):
		self._speed=sp
		self.manager.setSpeed(self.no,sp)
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
	@speed.setter 
	def hp(self,sp):
		self._hp=sp
	def SkillTo(self,skill,tragetNo):
		traget=manager.getUnit(tragetNo)
		arg=[traget,skill]
		for skill in self.f_beforeSkill:
				skill(arg)
		for skill in traget.f_beforeBeenSkill:
				skill(arg)
	def AfterSkillTo(self,skill,tragetNo)
		traget=manager.getUnit(tragetNo)
		arg=[traget,skill]
		for skill in self.f_beforeSkill:
			skill.trigger(arg)
		for skill in traget.f_beforeBeenSkill:
			skill.trigger(arg)
	def takeDamage(self,damage):
		for fuction in self.f_beforeTakeDamage:
			function(damage)
		if damage.exist:
			self.hp-=damage.num
		for fuction in self.f_beforeTakeDamage:
			function(damage)
	def causeDamage(tragetNo,kind,num):
		traget=self.manager.getUnit(tragetNo)
		if kind==damage.ATTACK_DAMAGE():
			num+=num*(self.power/100)
		elif kind==damage.SPECIAL_DAMAGE():
			num+=num*(self.intel/100)
		for fuction in self.f_beforeCauseDamage:
			function([traget,damage])
		traget.takeDamage(damage(kind,num,self))
		for fuction in self.f_afterCauseDamage:
			function([traget,damage])
class WarField(KBEngine.Entity):
	def shiftCallBack(self,no,x,y):
		self.shiftRecord[no]=[x,y]
	def __init__(self):
		KBEngine.Entity.__init__(self)
		DEBUG_MSG("WarField Cell done")
		self.space=XYCollied(2,4,-4*unit_radiu,-8*unit_radiu,4*unit_radiu,4*unit_radiu,self.shiftCallBack)#圆半径是10,格子宽度是两个圆也就是10*2 *2
		self.units=[]
		self.resigns=[]
		self.playerIds=[]
		self.cycle=0.1#更新周期
		self.timerId=self.addTimer(0.1,0.1,0)
		self.shiftRecord={}
		self.frame_num=1
		#除错代码
		for pos in default_debug:
			self.newUnit(0,[],pos.x,pos.y,0)
	def getUnit(self,no):
		for unit in self.units:
			if unit.no==no:
				return unit
		return None
	def onTimer( self, id, userArg ):
		#DEBUG_MSG("onUpdateBegin")
		#先做物理判定
		self.space.Collied()
		#主動技能觸發
		for unit in self.units:
			for s in self.skills:
				s.timeLeft-=self.manager.cycle
			for s in self.skills:
				if s.kind == skill.ACTIVE():
					s.trigger(None)#canUse自己在方法裏面判斷
		for unit in self.units:#主逻辑回圈,更新单位的AI,将单位速度和位移传给客户端
			#DEBUG_MSG("unit{0} center is {1}".format(unit.no,unit.circle.center))
			self.turnNo(unit.no)#该单位的更新周期开始
			#发送挤压的击退值
			#DEBUG_MSG("circle id{0} lastShiftx:{1} lastShifty:{2} center{3}".format(unit.circle.id,unit.circle.lastShiftx,unit.circle.lastShifty,str(unit.circle.center)))
			shift=self.shiftRecord[unit.circle.id]
			if not shift[0]==0 or not shift[1]==0:
				self.setShift(shift)
				self.shiftRecord[unit.circle.id]=[0,0]
			#再做速度移动
			if unit.moving:
				norm=unit.direct.normalized
				#debug代码
				if unit.no==1:
					DEBUG_MSG("norm is "+str(unit.direct.normalized))
					DEBUG_MSG("slave position before is {0}".format(self.units[1].circle.center))
				#------------------------
				unit.circle.center.x+=norm.x*unit.speed*self.cycle
				unit.circle.center.y+=norm.y*unit.speed*self.cycle
				#DEBUG_MSG("norm:({2},{3}) speed:({0},{1})".format(norm.x*unit.speed*self.cycle,norm.y*unit.speed*self.cycle,norm.x,norm.y))
			#debug代码
			if len(self.units)>1:
				DEBUG_MSG("slave position {0}".format(self.units[1].circle.center))
			#再做AI
			unit.update(self)
		for 
		self.updateEnd()
	def newUnit(self,rolekind,skillList,posx,posy,ownerid):
		circle=self.space.addCircle(Vector2(posx,posy),unit_radiu)
		unitNo=circle.id
		self.units.append(unit(circle,unitNo,self,ownerid))
		for pid in self.playerIds:
			DEBUG_MSG("pid is {0}".format(pid))
			KBEngine.entities[pid].p_addnewUnit(unitNo,rolekind,skillList,posx,posy,ownerid)
			#KBEngine.entities[pid].client.int64({"list":[90,99]})
	def playerSignIn(self,pid):
		self.playerIds.append(pid)
		#除错代码
		for unit in self.units:
			KBEngine.entities[pid].p_addnewUnit(unit.no,0,[],unit.circle.center.x,unit.circle.center.y,0)
	def playerSignOut(self,pid):
		self.playerIds.remove(pid)
	def setSpeed(self,new):
		DEBUG_MSG("setSpeed")
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setSpeed(new)
	def setDirect(self,new):
		DEBUG_MSG("setDirect {0}".format(new))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setDirect(new)
	def setShift(self,new):
		DEBUG_MSG("setShift {0}".format(new))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setShift(new)
	def setMoving(self,new):
		DEBUG_MSG("setMoving")
		for pid in self.playerIds:
			KBEngine.entities[pid].p_setMoving(new)
	def turnNo(self,no):
		DEBUG_MSG("turnNo")
		for pid in self.playerIds:
			KBEngine.entities[pid].p_turnNo(no)
	def useSkill(self,skillIndex,tragetNo):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_useSkill(skillIndex,tragetNo)
	def takeDamage(self,num):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_takeDamage(num)
	def beTreat(self,num):
		for pid in self.playerIds:
			KBEngine.entities[pid].p_beTreat(num)
	def updateEnd(self):
		DEBUG_MSG("update {0} end-----------------------------------------".format(self.frame_num))
		self.frame_num+=1
		for pid in self.playerIds:
			KBEngine.entities[pid].p_updateEnd(self.frame_num)
	def signUpTime(self,time,fuction,arg):
		self.resigns.append(time_resign(time,function,arg))
	def signUpArrow(self,speed,traget,oriPos,function,arg):
		self.resigns.append(arrow_resign(speed,traget,oriPos,function,arg))