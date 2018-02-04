from skill import skill
from AI import Event
import WarField

class no1_ATK(skill):
	@property
	def No(self):
		return 0#技能编号
	def __init__(self,radiu,unit,index):
		self.coolDown=1.0#技能冷却时间
		self.cdLeft=1.0#当前技能的剩余冷却时间
		self.kind=skill.ACTIVE()
		self.attack=True#是否是角色的基本攻击
		self.range=unit.AI.NEAR_RANGE(radiu)#攻击范围
		self.unit=unit
		self.index=index#技能在角色身上的欄位索引
	def canUse(self,arg):
		if self.AI==None or self.AI.traget==None or self.AI.LastSortList==None:
			print("AI 或 list为空")
			return False
		for pair in self.AI.LastSortList:
			if pair.key.id == self.AI.traget.id:
				if pair.value+pair.key.radiu <= self.range and cdLeft<=0
					return True
		return False
	def respons(self,traget):
			
	def trigger(self,arg):
		if self.canUse(arg):
		self.unit.manager.signUpTime(0.2,self.respons,self.unit.manager.getUnit(self.unit.AI.traget.id))#AI.traget的形态是圆但是id和它的unit相同
			self.unit.events.append(Event(self.unit.manager.useSkill,[]))
			self.unit.SkillTo(self,self.unit.AI.traget.id)
#正文--------------------------------------------------------------------------------------------
skillList=[no1_ATK]