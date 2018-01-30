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
		if self.traget==None or Vector2(center,traget.circle.center)>self.radiu+traget.circle.radiu:
			center=self.unit.circle.center
			print("do cast")
			dict=space.CastWithCloser(center.x,center.y,self.radiu)
			tragets=dict['answer']
			if(len(tragets)==0):#范围内没有目标
				self.traget=dict['closer']
			#搜寻后有攻击目标则移动
			if not self.traget==None:
				print("has traget after search")
				self.unit.direct=[traget.circle.center.x-unit.center.x,traget.circle.center.y-unit.center.y]
				if not self.unit.moving:
					self.unit.moving=True
			#无攻击目标
			else:
				self.unit.moving=False
				print("no traget")
		else:#有一个合理的攻击目标
			self.unit.moving=False
			print("has traget already")