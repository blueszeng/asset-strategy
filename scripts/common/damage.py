#Heavy <--penetration-->  light <--normal-->  cloth  <--magic-->  heavy  
#       -30%        +50%        -30%    +50%         -30%    +50%
class Damage:
	@staticmethod
	def NORMAL_DAMAGE():
		return 0
	@staticmethod
	def PENETRATION_DAMAGE():
		return 1
	@staticmethod
	def MAGIC_DAMAGE():
		return 2
	@staticmethod
	def REAL_DAMAGE():
		return 3
	@staticmethod
	def HEAVY_ARMOR():
		return 4
	@staticmethod
	def LIGHT_ARMOR():
		return 5
	@staticmethod
	def CLOTH_ARMOR():
		return 6
	@staticmethod
	def calVulnerable(damage,armorKind):
		if damage.kind == Damage.NORMAL_DAMAGE():
			if armorKind == Damage.LIGHT_ARMOR():
				damage.num -= int(damage.num*0.3)
			elif armorKind ==Damage.CLOTH_ARMOR():
				damage.num += int(damage.num*0.5)
			
		elif damage.kind == Damage.PENETRATION_DAMAGE():
			if armorKind == Damage.HEAVY_ARMOR():
				damage.num -= int(damage.num*0.3)
			elif armorKind == Damage.LIGHT_ARMOR():
				damage.num += int(damage.num*0.5)
			
		elif damage.kind == Damage.MAGIC_DAMAGE():
			if armorKind == Damage.CLOTH_ARMOR():
				damage.num -= int(damage.num*0.3)
			elif armorKind == Damage.HEAVY_ARMOR():
				damage.num += int(damage.num*0.5)
	@staticmethod
	def calAdditon(damage,power):
		damage.num+=int(damage.num*(power/100))
	@staticmethod
	def calReduce(damage,armor):
		print("armor {1} in calreduce {0}".format(armor/(armor+100),armor))
		damage.num-=int(damage.num*(armor/(armor+100)))
	def __init__(self,kind,num,damager):
		self.damager=damager
		self.num=num
		self.kind=kind
		self.exist=True