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
			unit.circle.f_onColliedIn.remove(self.LastCallBack)
		if not onHit == None:
			unit.circle.f_onColliedIn.append(onHit)
		if not self.onTheEnd == None:
			self.onTheEnd()
		self.onTheEnd=onTheEnd
		self.unit.events.append(Event(self.unit.manager.beRepel,[arraw,time]))#arraw是Vector2
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
				unit.circle.f_onColliedIn.remove(self.LastCallBack)
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
		self.f_beforeBeenSkill=[]
		self.f_afterBeenSkill=[]
		self.f_beforeTakeDamage=[]
		self.f_afterTakeDamage=[]
		self.f_beforeCauseDamage=[]
		self.f_afterCauseDamage=[]
		self.f_beforeSkill=[]
		self.f_afterSkill=[]
		self.f_beforeHealing=[]
		self.f_afterHealing=[]
		self.f_beforeBeenHealing=[]
		self.f_afterBeenHealing=[]
		#属性变量
		self._speed=self.STAND_SPEED
		self._hp=100
		self.repel=Repel(self)#被强迫的位移
		#self.repel=None
	def initSkill(self,list):
		for i in range(0,len(list)):
			nowSkill=skillList[list[i]](self.circle.radiu,self,i)
			DEBUG_MSG("on initskill {0}".format(i))
			#主動技能不註冊
			#註冊觸發方法
			if nowSkill.kind==Skill.BEFORE_BEEN_SKILL():
				self.f_beforeBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.AFTER_BEEN_SKILL():
				self.f_afterBeenSkill.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.BEFORE_TAKE_DAMAGE():
				self.f_beforeTakeDamage.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.AFTER_TAKE_DAMAGE():
				self.f_afterTakeDamage.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.BEFORE_CAUSE_DAMAGE():
				self.f_beforeCauseDamage.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.AFTER_CAUSE_DAMAGE():
				self.f_afterCauseDamage.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.BEFORE_SKILL():
				self.f_beforeSkill.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.AFTER_SKILL():
				self.f_afterSkill.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.BRFORE_HEAL():
				self.f_beforeHealing.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.AFTER_HEAL():
				self.f_beforeHealing.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.BRFORE_BEEN_HEAL():
				self.f_beforeBeenHealing.append(nowSkill.trigger)
			elif nowSkill.kind==Skill.AFTER_BEEN_HEAL():
				self.f_afterBeenHealing.append(nowSkill.trigger)
			self.skills.append(nowSkill)
	def initProperty(self,power,armor,armor_kind,physique,range=AI.NEAR_RANGE(unit_radiu)):
		self.power=power
		self.armor=armor
		self.armor_kind=armor_kind
		self.physique=physique
		self.AI=AI(self,range)
	def update(self,space):
		if not self.AI == None:#更新AI
			#print("no{0} AI update".format(self.no))
			self.AI.update(space)
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
		traget=self.manager.getUnit(tragetNo)
		arg=[skill,traget]
		for skill in self.f_beforeSkill:
				skill(arg)
		for skill in traget.f_beforeBeenSkill:
				skill(arg)
		self.events.append(Event(self.manager.useSkill,[skill.index,tragetNo]))
	def AfterSkillTo(self,skill,tragetNo):
		traget=self.manager.getUnit(tragetNo)
		arg=[skill,traget]
		for skill in self.f_beforeSkill:
			skill.trigger(arg)
		for skill in traget.f_beforeBeenSkill:
			skill.trigger(arg)
	def takeDamage(self,damage):
		for function in self.f_beforeTakeDamage:
			function(damage)
		if damage.exist:
			self.hp-=damage.num
			self.events.append(Event(self.manager.takeDamage,damage.num))
		for function in self.f_afterTakeDamage:
			function(damage)
	def beHealing(self,healpoint):
		for function in self.f_beforeBeenHealing:
			function(healpoint)
		if healpoint.exist:
			self.hp-=healpoint.num
			self.events.append(Event(self.manager.beTreat,healpoint.num))
		for function in self.f_afterBeenHealing:
			function(healpoint)
		
	def healingTo(self,tragetNo,num):
		print("heal tragetNo is {0}".format(tragetNo))
		traget=self.manager.getUnit(tragetNo)
		healpoint=Damage(2,num,self)
		for function in self.f_beforeHealing:
			function([traget,healpoint])
		traget.beHealing(healpoint)
		for function in self.f_afterHealing:
			function([traget,healpoint])
	def causeDamage(self,tragetNo,kind,num):
		print("cause tragetNo is {0}".format(tragetNo))
		traget=self.manager.getUnit(tragetNo)
		newd=Damage(kind,int(num),self)
		Damage.calAdditon(newd,self.power)
		Damage.calVulnerable(newd,traget.armor_kind)
		for function in self.f_beforeCauseDamage:
			function([traget,newd])
		traget.takeDamage(newd)
		for function in self.f_afterCauseDamage:
			function([traget,newd])
	def addBuff(self,buffClass,time,creater):
		#other.buffs[buffList.burn.no()]=buffList.burn(5,other,self.unit)#添加一个新的燃烧buff
		buff=buffClass(time,self,creater)
		self.buffs[buff.no()]=buff
		self.events.append(Event(self.manager.addBuff,buff.no()))
	def deleteBuff(self,buff):
		self.disabledBuffNo.append(buff.no())
		self.events.append(Event(self.manager.deleteBuff,buff.no()))
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
		i=0
		for pos in default_debug:
			self.newUnit(1,pos.x,pos.y,47+i)
			i+=1
	def getUnit(self,no):
		for unit in self.units:
			if unit.no==no:
				return unit
		return None
	def onTimer( self, id, userArg ):
		#先做物理判定
		self.space.Collied()
		#處理之前註冊的record
		for record in self.resigns:
			if record.update(self.cycle):
				self.resigns.remove(record)
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
			#更新技能
			print("no{0} events has {1} event".format(unit.no,len(unit.events)))
			for event in unit.events:
				event.funcion(event.arg)
				unit.events.remove(event)
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
				#DEBUG_MSG("no{0}".format(unit.no))
				#DEBUG_MSG("norm is "+str(unit.direct.normalized))
				#------------------------
				unit.circle.center.x+=norm.x*unit.speed*self.cycle
				unit.circle.center.y+=norm.y*unit.speed*self.cycle
				#DEBUG_MSG("norm:({2},{3}) speed:({0},{1})".format(norm.x*unit.speed*self.cycle,norm.y*unit.speed*self.cycle,norm.x,norm.y))
			#debug代码
			#DEBUG_MSG("position after is {0}".format(unit.circle.center))
			#再做AI
			unit.update(self)
		for unit in self.units:
			DEBUG_MSG("no{0} final position:{1}".format(unit.no,unit.circle.center))
		self.updateEnd()
	def newUnit(self,rolekind,posx,posy,ownerid):
		circle=self.space.addCircle(Vector2(posx,posy),unit_radiu)
		unitNo=circle.id
		newone=unit(circle,unitNo,self,ownerid)
		DEBUG_MSG("**new unit rolekind{0} list{1}".format(rolekind,skillNumberList.list[rolekind]))
		newone.initProperty(0,0,Damage.LIGHT_ARMOR(),0,skillNumberList.ranges[rolekind])
		newone.initSkill(skillNumberList.list[rolekind])
		self.units.append(newone)
		for pid in self.playerIds:
			DEBUG_MSG("pid is {0}".format(pid))
			KBEngine.entities[pid].p_addnewUnit(unitNo,rolekind,skillNumberList.list[rolekind],posx,posy,ownerid)
			#KBEngine.entities[pid].client.int64({"list":[90,99]})
	def playerSignIn(self,pid):
		self.playerIds.append(pid)
		rolekind=1
		#除错代码
		for unit in self.units:
			KBEngine.entities[pid].p_addnewUnit(unit.no,rolekind,skillNumberList.list[rolekind],unit.circle.center.x,unit.circle.center.y,0)
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
	def updateEnd(self):
		DEBUG_MSG("update {0} end-----------------------------------------".format(self.frame_num))
		for pid in self.playerIds:
			KBEngine.entities[pid].p_updateEnd(self.frame_num)
		self.frame_num+=1
	def signUpTime(self,time,function,arg):
		self.resigns.append(time_resign(time,function,arg))
	def signUpArrow(self,speed,traget,oriPos,function,arg):
		self.resigns.append(arrow_resign(speed,traget,oriPos,function,arg))