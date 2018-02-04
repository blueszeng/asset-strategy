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
		self.LastSortList=None#最近一次从近到远排序列
	def update(self,manager):
		space=manager.space
		#print("Enter AI update {0}".format(self.unit.no))
		center=self.unit.circle.center
		#如果没有目标(第一次)或原攻击目标超出范围
		if self.traget==None or (self.traget.center-center).magnitude>self.radiu+self.traget.radiu:
			list=space.getSortedCircleList(center,self.radiu)
			self.LastSortList=list
			for pair in list:
				if not manager.getUnit(pair.key.id).ownerid==self.unit.ownerid:#pair.key形态是Circle,value形态是float
					self.traget= manager.getUnit(pair.key.id).circle#把最近的那个设为目标
					break
			#搜寻后有攻击目标则移动
			if not self.traget==None:
				print("has traget after search--1")
				self.unit.direct=[self.traget.center.x-center.x,self.traget.center.y-center.y]
				if not self.unit.moving:
					self.unit.moving=True
			#无攻击目标
			else:
				self.unit.moving=False
				print("no traget--2")
		else:#有一个合理的攻击目标
			self.unit.moving=False
			print("has traget already--3")
class Event:
	def __init__(self,funcion,arg):
		self.funcion=funcion
		self.arg=arg