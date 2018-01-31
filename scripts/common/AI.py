from ColliedSpace import Vector2
class AI:
	@staticmethod
	def	NEAR_RANGE(radiu):
		return 1.5*radiu
	@staticmethod
	def FAR_RANGE(radiu):
		return 3.5*radiu
		
	def __init__(self,unit,unit_radiu):
		self.unit=unit
		self.traget=None
		self.radiu=unit_radiu#这是攻击区域半径,不是碰撞体半径
	def update(self,space):
		print("Enter AI update {0}".format(self.unit.no))
		center=self.unit.circle.center
		#如果没有目标(第一次)或原攻击目标超出范围
		if self.traget==None or (self.traget.center-center).magnitude>self.radiu+self.traget.radiu:
			dict=space.CastWithCloser(center.x,center.y,self.radiu)
			print("cast result:closer{0} answer{1} len(traget)={2}".format(dict['closer'],dict['answer'],len(dict['answer'])))
			tragets=dict['answer']
			if(len(tragets)==0):#范围内没有目标
				self.traget=dict['closer']
			else:#范围内有目标找到最近的那个
				nearest=None
				nearest_distant=0
				for circle in tragets:
					distant=(circle.center-center).magnitude#目标圆心减圆心的绝对值
					if nearest==None or distant<nearest_distant:#第一次计算或发现一个比nearest还y要近的圆
						print("set nearest")
						nearest= circle
						nearest_distant=distant
				self.traget=nearest#把最近的那个设为目标
			#搜寻后有攻击目标则移动
			if not self.traget==None:
				print("has traget after search")
				self.unit.direct=[self.traget.center.x-center.x,self.traget.center.y-center.y]
				if not self.unit.moving:
					self.unit.moving=True
			#无攻击目标
			else:
				self.unit.moving=False
				print("no traget")
		else:#有一个合理的攻击目标
			self.unit.moving=False
			print("has traget already")