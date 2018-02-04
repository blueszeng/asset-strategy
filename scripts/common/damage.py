class damage:
	@staticmethod
	def ATTACK_DAMAGE():
		return 0
	@staticmethod
	def SPECIAL_DAMAGE():
		return 1
	def REAL_DAMAGE():
		return 2
	def __init__(self,kind,num,damager):
		self.damager=damager
		self.num=num
		self.kind=kind
		self.exist=True