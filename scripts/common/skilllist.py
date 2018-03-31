from skill import Skill
from AI import Event
from damage import Damage
from ColliedSpace import Vector2
import WarField
import math
import random
import buffList
class General_combat_atk(Skill):
	def __init__(self,radiu,unit,index):
		#子类别客制化属性
		self.coolDown=1.0#技能冷却时间
		self.cdLeft=1.0#当前技能的剩余冷却时间
		self.damageKind=Damage.NORMAL_DAMAGE()
		self.damageNum=10
		self.timeBefore=0.2
		#固有代码
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		print("in no0 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or not self.unit.canAttack or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				if self.unit.manager.getUnit(pair.key.id)==None:
					return False
				print("value{0} radiu{1} range{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	def respons(self,tragetId):
		print("in skill no0 reapons roleid{0}".format(self.unit.no))
		self.unit.causeDamage(tragetId,self.damageKind,self.damageNum)
		self.unit.AfterSkillTo(self,tragetId)
	def trigger(self,arg):
		if self.canUse(arg):
			print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpTime(self.timeBefore,self.respons,self.unit.AI.traget.id)#AI.traget的形态是圆但是id和它的unit相同
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			self.cdLeft=self.coolDown
	def onTime(self,time):
		self.cdLeft-=time
class General_remote_atk(Skill):
	def __init__(self,radiu,unit,index):
		#客制化属性
		self.coolDown=1.5#技能冷却时间
		self.cdLeft=1.5#当前技能的剩余冷却时间
		self.damageKind=Damage.MAGIC_DAMAGE()
		self.damageNum=10
		self.missileSpeed=5
		#固有代码
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.FAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		print("in no5 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				if self.unit.manager.getUnit(pair.key.id)==None:
					return False
				#("value{0} radiu{1} range>{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		#print("in no5 canUse return false!!!!!")
		return False
	def respons(self,tragetId):
		print("self is {0}".format(self))
		#print("in skill no0 reapons roleid{0}".format(self.unit.no))
		self.unit.causeDamage(tragetId,self.damageKind,self.damageNum)
		self.unit.AfterSkillTo(self,tragetId)
	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpArrow(self.missileSpeed,self.unit.AI.traget,self.unit.circle.center,self.respons,self.unit.AI.traget.id)#AI.traget的形态是圆但是id和它的unit相同
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			self.cdLeft=self.coolDown
	def onTime(self,time):
		self.cdLeft-=time
class no1_ATK(General_combat_atk):
	@property
	def No(self):
		return 0#技能编号
	def __init__(self,radiu,unit,index):
		super().__init__(radiu,unit,index)
		self.coolDown=1.0#技能冷却时间
		self.cdLeft=1.0#当前技能的剩余冷却时间
		self.damageKind=Damage.NORMAL_DAMAGE()
		self.damageNum=10
		self.timeBefore=0.2

class no2_flamechop(Skill):
	def No(self):
		return 1#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=4.0#技能冷却时间
		self.cdLeft=4.0#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=2*radiu#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				if self.unit.manager.getUnit(pair.key.id)==None:
					return False
				#print("value{0} radiu{1} range{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	def respons(self,null):
		for pair in self.unit.LastSortList:
			if (not self.unit.manager.getUnit(pair.key.id).ownerid==self.unit.ownerid)and  pair.value <= self.range +pair.key.radiu:
				traget=self.unit.manager.getUnit(pair.key.id)
				#print("in skill no2 self id{0} traget id{1} dir{2}".format(self.unit.no,traget.no,self.unit.direct))
				#v1=self.unit.direct
				#v2=traget.circle.center-self.unit.circle.center
				#print("v1*v2:{0} m1*m2:{1} ans:{2}".format(v1*v2,v1.magnitude*v2.magnitude,(v1*v2)/(v1.magnitude*v2.magnitude)))
				if not traget==None and Vector2.angleBetween(self.unit.direct,traget.circle.center-self.unit.circle.center)<=math.pi*0.5:
					self.unit.causeDamage(traget.no,Damage.MAGIC_DAMAGE(),16)
					self.unit.AfterSkillTo(self,traget.no)
	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpTime(0.3,self.respons,None)#AI.traget的形态是圆但是id和它的unit相同
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			self.cdLeft=self.coolDown
	def onTime(self,time):
		self.cdLeft-=time
class no3_gush(Skill):
	def No(self):
		return 2#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=6.0#技能冷却时间
		self.cdLeft=6.0#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=4#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		if self.cdLeft<=0:
			return True
		#print("canUse return false!!!!!")
		return False
	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpTime(0.3,self.respons,None)#AI.traget的形态是圆但是id和它的unit相同
			self.unit.SkillTo(self,self.unit.no)
			self.cdLeft=self.coolDown
	def respons(self,null):
		for pair in self.unit.LastSortList:
			traget=self.unit.manager.getUnit(pair.key.id)
			if (not traget ==None and traget.ownerid==self.unit.ownerid)and  pair.value <= self.range +pair.key.radiu:
				self.unit.healingTo(traget.no,25)
				self.unit.AfterSkillTo(self,traget.no)
	def onTime(self,time):
		self.cdLeft-=time
class no4_elementProtect(Skill):
	def No(self):
		return 3#技能编号
	def __init__(self,radiu,unit,index):
		self.kind=Skill.BEFORE_TAKE_DAMAGE()
		self.attack=True#是否是角色的基本攻击
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def trigger(self,damage):
			#print("in role{0} skill trigger:::::::::::::::::::::::::{0}".format(self.unit.no))
			if damage.kind==Damage.MAGIC_DAMAGE():
				if random.randint(1,100)<=65:#50%几率
					#print("is magic damage")
					self.unit.events.append(Event(self.unit.manager.useSkill,[self.index,self.unit.no]))
					damage.exist=False#无效
	def onTime(self,time):
		pass
class no5_ATK2(General_remote_atk):
	@property
	def No(self):
		return 4#技能编号
	def __init__(self,radiu,unit,index):
		super().__init__(radiu,unit,index)
		self.coolDown=1.5#技能冷却时间
		self.cdLeft=1.5#当前技能的剩余冷却时间
		self.damageKind=Damage.MAGIC_DAMAGE()
		self.damageNum=10
		self.missileSpeed=5
class no6_hotWave(Skill):
	@property
	def No(self):
		return 5#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=6#技能冷却时间
		self.cdLeft=6#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		print("in no6 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			traget=self.unit.manager.getUnit(pair.key.id)
			if not traget == None and not self.unit.manager.getUnit(pair.key.id).ownerid==self.unit.ownerid:
				#print("value{0} radiu{1} range>{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		#print("canUse return false!!!!!")
		return False

	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.SkillTo(self,self.unit.no)
			for pair in self.unit.LastSortList:
				if not pair.key==None:
					if pair.value > self.range +pair.key.radiu:#因为是从小到大排序的list所以一旦出现比目标大的数之后只会更大
						break
					#如果还在范围内
					else:
						other=self.unit.manager.getUnit(pair.key.id)
						if not other ==None and not other.ownerid==self.unit.ownerid:#其他队角色
							arraw=(pair.key.center-self.unit.circle.center).normalized
							distant=Vector2(arraw.x*5,arraw.y*5)
							self.unit.manager.getUnit(pair.key.id).repel.begin(distant,0.3,None,None)
							self.cdLeft=self.coolDown
							if buffList.burn.no() in other.buffs.keys():#已经有buff burn 了
								other.buffs[buffList.burn.no()].timeLeft=5#重置之前燃烧的持续时间
							else:
								other.addBuff(buffList.burn,5,self.unit)
			self.unit.AfterSkillTo(self,self.unit.no)
	def onTime(self,time):
		self.cdLeft-=time
class no7_livingBomb(Skill):
	@property
	def No(self):
		return 6#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=4#技能冷却时间
		self.cdLeft=4#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.FAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		#print("in no7 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			if pair.key.id == self.unit.AI.traget.id and not self.unit.manager.getUnit(self.unit.AI.traget.id)==None:
				#print("value{0} radiu{1} range{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		#print("canUse return false!!!!!")
		return False

	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpTime(0.3,self.respons,self.unit.manager.getUnit(self.unit.AI.traget.id))
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			self.cdLeft=self.coolDown
	def respons(self,other):
		#print("in livingBomb respons")
		if buffList.bombCounter.no() in other.buffs.keys():#已经被活体炸弹了
			#print(">go re")
			other.buffs[buffList.bombCounter.no()].redetonate(3)#重新引爆
			other.events.append(Event(self.unit.manager.deleteBuff,buffList.bombCounter.no()))
			other.events.append(Event(self.unit.manager.addBuff,buffList.bombCounter.no()))
		else:
			#print(">go add")
			other.addBuff(buffList.bombCounter,3,self.unit)
		self.unit.AfterSkillTo(self,other.no)
	def onTime(self,time):
		self.cdLeft-=time
class no8_MolotovCocktail(Skill):
	@property
	def No(self):
		return 7#技能编号
	def __init__(self,radiu,unit,index):
		self.kind=Skill.AFTER_SKILL()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.FAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
		self.traget=None
	def canUse(self,arg):
		#print("in no7 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			now=self.unit.manager.getUnit(pair.key.id)
			if not now==None and not now.ownerid == self.unit.ownerid:
				if pair.value <= self.range +pair.key.radiu:
					self.traget=now
					return True
				else:
					#print("canUse return false!!!!!")
					return False
	def trigger(self,arg):
		if self.canUse(arg):
			if random.randint(1,100)<=25:#25%几率
				#print("in no8 skill trigger roleid{0}".format(self.unit.no))
				self.unit.manager.signUpArrow(4,self.traget.circle,self.unit.circle.center,self.respons,self.traget)
				self.unit.SkillTo(self,self.unit.AI.traget.id)
	def respons(self,other):
		self.unit.causeDamage(other.no,Damage.MAGIC_DAMAGE(),15)
		for pair in other.LastSortList:
			if pair.value <= 3+pair.key.radiu:
				if not  self.unit.manager.getUnit(pair.key.id)==None and not self.unit.manager.getUnit(pair.key.id).ownerid == self.unit.ownerid:
					self.unit.causeDamage(pair.key.id,Damage.MAGIC_DAMAGE(),15)
			else:
				break
	def onTime(self,time):
		pass
class no9_dash(Skill):
	def __init__(self,radiu,unit,index):
		self.coolDown=5.0#技能冷却时间
		self.cdLeft=0#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	@property
	def No(self):
		return 8#技能编号
	def canUse(self,arg):
		print("in no0 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or not self.unit.canAttack or self.unit.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				if self.unit.manager.getUnit(pair.key.id)==None:
					return False
				print("value{0} radiu{1} range{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value > self.range +pair.key.radiu and self.cdLeft<=0:
					print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	def onhit(self,selfcircle,other):
		print("hhhhhhh onhit is really been call.. hhhhhhh")
		traget=self.unit.manager.getUnit(other.id)
		if not buffList.coma.no() in traget.buffs.keys():
			traget.addBuff(buffList.coma,1,self.unit)
		else:
			traget.buffs[buffList.coma.no()].timeLeft=1
		arraw=(other.center-selfcircle.center).normalized
		traget.repel.begin(arraw.scaleWith(0.8),0.2,None,None)
	def trigger(self,arg):
		if self.canUse(arg):
			print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			arraw=self.unit.AI.traget.center- self.unit.circle.center
			self.unit.repel.begin(Vector2(arraw.normalized.x*5,arraw.normalized.y*5),0.5,self.onhit,None)
			self.cdLeft=self.coolDown
	def onTime(self,time):
		self.cdLeft-=time
class no10_normal_Atk(General_combat_atk):
	def __init__(self,radiu,unit,index):
		super().__init__(radiu,unit,index)

	@property
	def No(Self):
		return 12
		
class no11_swept(Skill):
	def __init__(self,radiu,unit,index):
		self.kind = Skill.AFTER_SKILL()
		self.unit = unit
		self.range=unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.index=index#技能在角色身上的欄位索引
	
	def trigger(self,list):
		skill = list[0]
		traget = list[1]
		if skill.attack:
			for pair in self.unit.LastSortList:
				if pair.value <= self.range + pair.key.radiu:
					print("aaaaa:",pair.key.id)
					
					
					if (not (self.unit.manager.getUnit(pair.key.id).ownerid == self.unit.ownerid)) and (not (
								self.unit.manager.getUnit(pair.key.id).no == traget.no)):#異類即是仇敵
						positiveDirection = self.unit.direct
						targetDirection = self.unit.manager.getUnit(pair.key.id).circle.center - self.unit.circle.center
						targetAngle = Vector2.angleBetween(positiveDirection,targetDirection)
						
						if (targetAngle <= 90):
							print("aaaaa:omg",pair.key.id)
							targetNum = pair.key.id
							self.unit.causeDamage(targetNum,Damage.NORMAL_DAMAGE(),10)
			self.unit.SkillTo(self, traget.no)
	def onTime(self,time):
		pass

	@property
	def No(Self):
		return 13
		
class no12_regeneration(Skill):
	def __init__(self,radiu,unit,index):
		self.kind = Skill.AFTER_SKILL()
		self.unit = unit
		self.range = unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.index = index#技能在角色身上的欄位索引
		self.coolDown = 1.0
		self.cdTime = 1.0#当前技能的剩余冷却时间
	
	def trigger(self,list):
		traget = list[1]
		if self.cdTime <= 0:
			self.unit.healingTo(self.unit.no, 5)
			self.cdTime = self.coolDown
		
	def onTime(self,time):
		self.cdTime -= time

	@property
	def No(Self):
		return 14


class no13_multiArrow(General_remote_atk):
	@property
	def No(self):
		return 9#技能编号
	def __init__(self,radiu,unit,index):
		super().__init__(radiu,unit,index)
		self.coolDown=4#技能冷却时间
		self.cdLeft=4#当前技能的剩余冷却时间
		self.damageKind=Damage.PENETRATION_DAMAGE()
		self.damageNum=8
		self.missileSpeed=8
	def trigger(self,arg):
		tragets=[]
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			for pair in self.unit.LastSortList:
				if pair.value <= self.range +pair.key.radiu:
					if not self.unit.manager.getUnit(pair.key.id).ownerid==self.unit.ownerid:#異類即是仇敵
						self.unit.manager.signUpArrow(self.missileSpeed,pair.key,self.unit.circle.center,self.respons,pair.key.id)#AI.traget的形态是圆但是id和它的unit相同
						tragets.append(pair.key.id)
				else:
					break
			self.unit.SkillTo(self,tragets)
			self.cdLeft=self.coolDown
class no14_ATK4(General_remote_atk):
	def No(self):
		return 10#技能编号
	def __init__(self,radiu,unit,index):
		super().__init__(radiu,unit,index)
		self.coolDown=1.0#技能冷却时间
		self.cdLeft=1.0#当前技能的剩余冷却时间
		self.damageKind=Damage.PENETRATION_DAMAGE()
		self.damageNum=10
		self.missileSpeed=10
class no15_precisionStrike(Skill):
	def No(self):
		return 11
	def __init__(self,radiu,unit,index):
		self.kind=Skill.AFTER_CAUSE_DAMAGE()
		self.attack=True#是否是角色的基本攻击
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def trigger(self,list):
		damage=list[1]
		if damage.kind==Damage.PENETRATION_DAMAGE():
			traget=list[0]
			traget.causeDamage(traget.no,Damage.REAL_DAMAGE(),5)
			self.unit.events.append(Event(self.unit.manager.createEffection,[ 0 ,traget.no]))#針對traget 創造編號0的效果
	def onTime(self,time):
		pass
#正文--------------------------------------------------------------------------------------------
skillList=[no1_ATK,no2_flamechop,no3_gush,no4_elementProtect,no5_ATK2,no6_hotWave,no7_livingBomb,
		no8_MolotovCocktail,no9_dash,no13_multiArrow,no14_ATK4,no15_precisionStrike,no10_normal_Atk, no11_swept, no12_regeneration]