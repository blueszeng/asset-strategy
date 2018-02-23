class Skill:
	@staticmethod
	def EVERY_FRAME():
		return 0
	@staticmethod
	def ACTIVE():
		return 1
	@staticmethod
	def BEFORE_BEEN_SKILL():
		return 2
	@staticmethod
	def AFTER_BEEN_SKILL():
		return 3
	@staticmethod
	def BEFORE_TAKE_DAMAGE():
		return 4
	@staticmethod
	def AFTER_TAKE_DAMAGE():
		return 5
	@staticmethod
	def BEFORE_SKILL():
		return 6
	@staticmethod
	def AFTER_SKILL():
		return 7
	@staticmethod
	def BEFORE_CAUSE_DAMAGE():
		return 8
	@staticmethod
	def AFTER_CAUSE_DAMAGE():
		return 9
	@staticmethod
	def BRFORE_HEAL():
		return 10
	@staticmethod
	def AFTER_HEAL():
		return 11
	@staticmethod
	def BRFORE_BEEN_HEAL():
		return 12
	@staticmethod
	def AFTER_BEEN_HEAL():
		return 13
	def __init__(self):
		self.coolDown=0#技能冷却时间
		self.cdLeft=0#当前技能的剩余冷却时间
		self.kind=self.ACTIVE()
		self.attack=False#是否是角色的基本攻击
	def canUse(self,arg):
		pass
	def trigger(self,arg):
		pass
	def respons(self,arg):
		pass
