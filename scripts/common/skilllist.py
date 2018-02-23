from skill import Skill
from AI import Event
from damage import Damage
from ColliedSpace import Vector2
import WarField
import math
import random
import buffList
class no1_ATK(Skill):
	@property
	def No(self):
		return 0#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=1.0#技能冷却时间
		self.cdLeft=1.0#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		print("in no0 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.AI.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.AI.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				print("value{0} radiu{1} range{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	def respons(self,tragetId):
		print("in skill no0 reapons roleid{0}".format(self.unit.no))
		self.unit.causeDamage(tragetId,Damage.NORMAL_DAMAGE(),10)
		self.unit.AfterSkillTo(self,tragetId)
	def trigger(self,arg):
		if self.canUse(arg):
			print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpTime(0.2,self.respons,self.unit.AI.traget.id)#AI.traget的形态是圆但是id和它的unit相同
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			self.cdLeft=self.coolDown
	def onTime(self,time):
		self.cdLeft-=time
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
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.AI.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.AI.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				#print("value{0} radiu{1} range{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	def respons(self,null):
		for pair in self.unit.AI.LastSortList:
			if (not self.unit.manager.getUnit(pair.key.id).ownerid==self.unit.ownerid)and  pair.value <= self.range +pair.key.radiu:
				traget=self.unit.manager.getUnit(pair.key.id)
				#print("in skill no2 self id{0} traget id{1} dir{2}".format(self.unit.no,traget.no,self.unit.direct))
				#v1=self.unit.direct
				#v2=traget.circle.center-self.unit.circle.center
				#print("v1*v2:{0} m1*m2:{1} ans:{2}".format(v1*v2,v1.magnitude*v2.magnitude,(v1*v2)/(v1.magnitude*v2.magnitude)))
				if Vector2.angleBetween(self.unit.direct,traget.circle.center-self.unit.circle.center)<=math.pi*0.5:
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
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.AI.LastSortList==None:
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
		for pair in self.unit.AI.LastSortList:
			if (self.unit.manager.getUnit(pair.key.id).ownerid==self.unit.ownerid)and  pair.value <= self.range +pair.key.radiu:
				traget=self.unit.manager.getUnit(pair.key.id)
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
				if random.randint(1,100)<=50:#50%几率
					#print("is magic damage")
					self.unit.events.append(Event(self.unit.manager.useSkill,[self.index,self.unit.no]))
					damage.exist=False#无效
	def onTime(self,time):
		pass
class no5_ATK2(Skill):
	@property
	def No(self):
		return 4#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=1.5#技能冷却时间
		self.cdLeft=1.5#当前技能的剩余冷却时间
		self.kind=Skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.FAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		print("in no0 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.AI.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.AI.LastSortList:
			if pair.key.id == self.unit.AI.traget.id:
				print("value{0} radiu{1} range>{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	def respons(self,tragetId):
		#print("in skill no0 reapons roleid{0}".format(self.unit.no))
		self.unit.causeDamage(tragetId,Damage.NORMAL_DAMAGE(),12)
		self.unit.AfterSkillTo(self,tragetId)
	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.manager.signUpArrow(5,self.unit.AI.traget,self.unit.circle.center,self.respons,self.unit.AI.traget.id)#AI.traget的形态是圆但是id和它的unit相同
			self.unit.SkillTo(self,self.unit.AI.traget.id)
			self.cdLeft=self.coolDown
	def onTime(self,time):
		self.cdLeft-=time
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
		print("in no0 skill canUse roleid{0}".format(self.unit.no))
		if self.unit.AI==None or self.unit.AI.traget==None or self.unit.AI.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.unit.AI.LastSortList:
			if not self.unit.manager.getUnit(pair.key.id).ownerid==self.unit.ownerid:
				print("value{0} radiu{1} range>{2} time{3}".format(pair.value,pair.key.radiu,self.range,self.cdLeft))
				if pair.value <= self.range +pair.key.radiu and self.cdLeft<=0:
					#print("canUse return true!!!!!")
					return True
		print("canUse return false!!!!!")
		return False
	
	def trigger(self,arg):
		if self.canUse(arg):
			#print("in no0 skill trigger roleid{0}".format(self.unit.no))
			self.unit.SkillTo(self,self.unit.no)
			for pair in self.unit.AI.LastSortList:
				if pair.value > self.range +pair.key.radiu:#因为是从小到大排序的list所以一旦出现比目标大的数之后只会更大
					break
				#如果还在范围内
				else:
					other=self.unit.manager.getUnit(pair.key.id)
					if not other.ownerid==self.unit.ownerid:#其他队角色
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
#正文--------------------------------------------------------------------------------------------
skillList=[no1_ATK,no2_flamechop,no3_gush,no4_elementProtect,no5_ATK2,no6_hotWave]