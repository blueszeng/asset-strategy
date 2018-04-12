import math

import sys

import XYTree
import time
class Pair:
	def __init__(self,key,value):
		self.key=key
		self.value=value
	def __str__(self):
		return "id{0}:{1}".format(self.key.id,self.value)
class Circle:
	@property
	def center(self):
		return self._center
	@center.setter
	def center(self,new):
		x=self._center.x
		y=self._center.y
		self._center=new
		self.lastX=x
		self.lastY=y
		if not self.onCenterChange==None:
			self.onCenterChange(self)
	def centerChange(self,oriX,oriY,v):#参数是Vector2
		self.lastX=oriX
		self.lastY=oriY
		self.onCenterChange(self)
	def __init__(self,center,radiu,id,callBack=None):#id用來快速檢索closeset
		self.onCenterChange=callBack#当圆心改变时呼叫,参数是Circle
		self._center=center
		self._center.onChange=self.centerChange#这样是因为直接改center.x或y时不会触发魔术方法
		self.radiu=radiu 
		self.id=id
		self.lastShiftx=0
		self.lastShifty=0
		self.lastFrameClosers=[]
		self.f_onColliedIn=[]
		self.f_onCenterChange=[]
	def __str__(self):
		return "id:"+str(self.id)+":"+str(self.center)+"radiu:"+str(self.radiu)

class Vector2:
	def __init__(self,x,y,callBack=None):
		self._x=x
		self._y=y
		self.magnitude=math.sqrt(x*x+y*y)#向量長度
		self.onChange=callBack
	@property
	def x(self):
		return self._x
	@x.setter
	def x(self,new):
		oriX=self._x
		self._x=new
		if not self.onChange==None:
			self.onChange(oriX,self._y,self)
	@property
	def y(self):
		return self._y
	@y.setter
	def y(self,new):
		oriY=self._y
		self._y=new
		if not self.onChange==None:
			self.onChange(self._x,oriY,self)
	@property
	def normalized(self):
		if self.magnitude==0:
			return Vector2(0,0)
		else:
			return Vector2(self.x/self.magnitude,self.y/self.magnitude)
	def __add__(self,other):
		return Vector2(self.x+other.x,self.y+other.y)
	def __sub__(self,other):
		return Vector2(self.x-other.x,self.y-other.y)
	def __mul__(self,other):#點積
			return self.x*other.x+self.y*other.y
	def __str__(self):
		return "({0},{1})".format(self.x,self.y)
	def __neg__(self):#反向量
		return Vector2(-self.x,-self.y)
	@staticmethod
	def distantBetween(first,second):
		#print(":::::::::::::::::::::::distantBetween")
		return math.sqrt((first.x-second.x)*(first.x-second.x)+(first.y-second.y)*(first.y-second.y))
	@staticmethod
	def angleBetween(first,second):
		#print("in angle first *second is{0}".format(first*second))
		#print("first mag:{0} second mag:{1}".format(first.magnitude,second.magnitude))
		#print("before acos ans is:{0}".format((first*second)/(first.magnitude*second.magnitude)))
		before=(first*second)/(first.magnitude*second.magnitude)
		if before>1 and before <1.0001:#去误差处理,之前有出现过因为1.000000002报数学范围错误的问题
			before=1
		elif before<-1 and before>-1.0001:
			before=-1
		return math.acos(before)
	def scaleWith(self,constant):
		self.x*=constant
		self.y*=constant
		self.magnitude*=constant
		return self
class CloseSetNode:#用於記錄哪些圓形與本圓形相鄰
	def __init__(self,owner):
		self.owner=owner
		self.closer=[]
		self.shift=Vector2(0,0)
		
class XYCollied:
	def __init__(self,xnum,ynum,left,up,width,height,shiftCallBack):
		self.circles=XYTree.XYTree(xnum,ynum,left,up,width,height)
		self.totalNum=0
		self.record=[]#因为扫整个树节点太慢了所以record将记录下在之下有圆的节点,遍历时直接线性遍历record
		self.closeSet={}
		self.halfdiagonal=math.sqrt((width/2)*(width/2)+(height/2)*(height/2))#半斜角距离
		self.shiftCallBack=shiftCallBack
	def onCircleChange(self,circle):
		#print("::: onCircleChange be call :::new x:{0} y:{1}".format(circle.center.x,circle.center.y))
		#print("lastX{0} lastY{1} x{2} y{3} the same{4}".format(circle.lastX,circle.lastY,circle.center.x,circle.center.y,self.circles.inSameArea(circle.lastX,circle.lastY,circle.center.x,circle.center.y)))
		if not self.circles.inSameArea(circle.lastX,circle.lastY,circle.center.x,circle.center.y):#如果移动之后会进入一个新的区域
			node=self.circles.getNode(circle.lastX,circle.lastY)
			node.subNode.remove(circle)
			if len(node.subNode)==0:
				self.record.remove(node)
			newnode=self.circles.getNode(circle.center.x,circle.center.y)
			newnode.subNode.append(circle)
			if not newnode in self.record:
				self.record.append(newnode)
			print("circle move from ({0},{1}) to ({2},{3})".format(node.getIndexX(self.circles),node.getIndexY(self.circles),newnode.getIndexX(self.circles),newnode.getIndexY(self.circles)))
			print("oripos({0},{1}) newpos({2},{3})".format(circle.lastX,circle.lastY,circle.center.x,circle.center.y))
			print("in - y is{0} y is{1}".format(circle.lastY-self.circles.upBoundary,circle.center.y-self.circles.upBoundary))
			print("y1/num{0} y2/num{1}".format(math.floor(circle.lastY/self.circles.cellHeight),math.floor(circle.center.y/self.circles.cellHeight)))
	def addCircle(self,position,radiu):
		if	len(self.circles.getNode(position.x,position.y).subNode)==0:#如果node里没有装载节点
			self.record.append(self.circles.getNode(position.x,position.y))
		circle=Circle(position,radiu,self.totalNum,self.onCircleChange)
		self.circles.addUnit(position.x,position.y,circle)
		self.totalNum+=1
		return circle
	def delCircle(self,circle):
		node=self.circles.getNode(circle.center.x,circle.center.y)
		node.subNode.remove(circle)
		if len(node.subNode)==0:
			self.record.remove(node)
	def ColliedWith(self,shift,circle,overSet):#用於遞迴分散位移
#建立CloseSet----------------------------------------------------------------------
		if(not circle.id in self.closeSet):#還未記錄自己的與相鄰列表
			node=self.circles.getNode(circle.center.x,circle.center.y)
			considerSet=node.subNode[:]#考虑集合,用来记录需要考虑的所有圆,只在建立closeSet中使用
			self.closeSet[circle.id]=CloseSetNode(circle)#新增屬於此圓相鄰集合的節點
			#计算可能碰撞的区域应该有4个这个推算建立于:所有圆都小于等于格子长的1/2
			xdir=0
			ydir=0
			if (not node.left==None) and (circle.center.x%self.circles.cellWidth)<=0.5*self.circles.cellWidth:#说明圆心在格子的左侧
				#print("enter left")
				xdir=-1
				considerSet+=node.left.subNode
			elif (not node.right==None) and (circle.center.x%self.circles.cellWidth)>0.5*self.circles.cellWidth:
				#print("enter right")
				xdir=1
				considerSet+=node.right.subNode
			if (not node.down==None) and circle.center.y%self.circles.cellHeight>0.5*self.circles.cellHeight:#下
				#print("enter down")
				ydir=-1
				considerSet+=node.down.subNode
			elif (not node.up==None) and circle.center.y%self.circles.cellHeight<=0.5*self.circles.cellHeight:
				#print("enter up")
				ydir=1
				considerSet+=node.up.subNode
			if	not xdir==0 and not ydir==0:
				if xdir>0:
					if ydir>0:#右上
						considerSet+=node.right.up.subNode
					else:
						considerSet+=node.right.down.subNode
				else:
					if ydir>0:#左上
						considerSet+=node.left.up.subNode
					else:
						considerSet+=node.left.down.subNode
			#print("considerSet is"+str(considerSet))
			for other in considerSet:#遍历考虑集合的所有圆
				if not other == circle:
					distant=Vector2.distantBetween(circle.center,other.center)
					if distant <=(circle.radiu+other.radiu):#距離小於等於半徑之和說明相交或相鄰
						self.closeSet[circle.id].closer.append(other)
						#如果上一帧记录中没有此圆
						if other not in circle.lastFrameClosers:
							for function in  circle.f_onColliedIn:
								function(circle,other)#逐个呼叫onColliedIn中的callback
		#记录closer到lastFrameClosers
		circle.lastFrameClosers=self.closeSet[circle.id].closer
		#給自己一個位移
		
		self.closeSet[circle.id].shift+=shift
		overSet.append(circle)#將自己標記成傳遞over
	#開始分散位移
		for other in self.closeSet[circle.id].closer:
			#print("shift:{0}other.center-circle.center:{1}".format(shift,other.center-circle.center))
			if not other in overSet and Vector2.angleBetween(shift,other.center-circle.center)<=(math.pi*0.5):#如果目標圓還沒有傳遞過,並且相對圓心和位移的夾角小於90度
				#print("{0}->{1}-------------------------------".format(circle.id,other.id))
				self.ColliedWith(shift,other,overSet)#去吧少年
	def Collied(self):
		#print(self.circles)
		self.closeSet={}#重置closeSet,相邻集合(CloseSet)用来记录一个圆相交或相邻的其他圆,用于计算击退和计算击退传递
		for node in self.record:#每個圓形只計算自己對其他圓形的擊退距離,和一個自己被反擊退的距離
			#print("node record:-------------------")
			for circle in node.subNode:
				#print("circle:"+str(circle))
				#建立CloseSet----------------------------------------------------------------------
				if(not circle.id in self.closeSet):#還未記錄自己的與相鄰列表
					considerSet=node.subNode[:]#考虑集合,用来记录需要考虑的所有圆,只在建立closeSet中使用
					self.closeSet[circle.id]=CloseSetNode(circle)#新增屬於此圓相鄰集合的節點
					#计算可能碰撞的区域应该有4个这个推算建立于:所有圆都小于等于格子长的1/2
					xdir=0
					ydir=0
					if (not node.left==None) and (circle.center.x%self.circles.cellWidth)<=0.5*self.circles.cellWidth:#说明圆心在格子的左侧
						#print("enter left")
						xdir=-1
						considerSet+=node.left.subNode
					elif (not node.right==None) and (circle.center.x%self.circles.cellWidth)>0.5*self.circles.cellWidth:
						#print("enter right")
						xdir=1
						considerSet+=node.right.subNode
					if (not node.down==None) and circle.center.y%self.circles.cellHeight>0.5*self.circles.cellHeight:#下
						#print("enter down")
						ydir=-1
						considerSet+=node.down.subNode
					elif (not node.up==None) and circle.center.y%self.circles.cellHeight<=0.5*self.circles.cellHeight:
						#print("enter up")
						ydir=1
						considerSet+=node.up.subNode
					if	not xdir==0 and not ydir==0:
						if xdir>0:
							if ydir>0:#右上
								considerSet+=node.right.up.subNode
							else:
								considerSet+=node.right.down.subNode
						else:
							if ydir>0:#左上
								considerSet+=node.left.up.subNode
							else:
								considerSet+=node.left.down.subNode
					#print("considerSet is"+str(considerSet))
					for other in considerSet:#遍历考虑集合的所有圆
						if not other == circle:
							distant=Vector2.distantBetween(circle.center,other.center)
							if distant <=(circle.radiu+other.radiu):#距離小於等於半徑之和說明相交或相鄰
								self.closeSet[circle.id].closer.append(other)
								#如果上一帧记录中没有此圆
								if other not in circle.lastFrameClosers:
									for function in  circle.f_onColliedIn:
										function(circle,other)#逐个呼叫onColliedIn中的callback
				#记录closer到lastFrameClosers
				circle.lastFrameClosers=self.closeSet[circle.id].closer
				#print("bf cal circle{0} position is{1}".format(circle.id,circle.center))
				#对所有与当前圆相邻的圆计算击退---------------------------------------------------------------
				for other in self.closeSet[circle.id].closer:
					#print("XYCollied {0}{1}->{2}{3}-------------------------------".format(circle.id,circle.center,other.id,other.center))
					#nowCenter對方當前推算過位移(shift)的圓心
					if other.id in self.closeSet:#這個判斷是為了防止對方還沒有記錄與closeSet中,沒記錄說明shift為無
						#print("推定另一shift为"+str(self.closeSet[circle.id].shift))
						nowCenter=other.center+self.closeSet[other.id].shift#這個nowCenter是根據當前位移和原圓心位置推導出來的當前圓心位置
					else:
						nowCenter=other.center
					
					#nowCircleCenter自己當前推算過位移(shift)的圓心
					#print("推定自己shift为"+str(self.closeSet[circle.id].shift))
					nowCircleCenter=circle.center+self.closeSet[circle.id].shift
					
					halfOverlap=(circle.radiu+other.radiu-Vector2.distantBetween(nowCircleCenter,nowCenter))/2#半徑之和減去圓心距離可知道兩個圓重疊半徑
					if round(halfOverlap,1) <=0:#如果舍去至一位小數後為0則不做,說明擠壓度太小了可以忽略,这样可以防止重复击退:A击退B,那么理论上A和B的距离应该为0,所以当B计算时会在这里略过A
						continue
					#print("halfOverlap is {0}".format(halfOverlap))
					orishift=((nowCenter-circle.center).normalized).scaleWith(halfOverlap)#放大指向目標圓心的單位向量,這將是本次的shift
					#print("origen shift is:{0}".format(orishift))
					#击退--------------------------------------------
					over=[circle]#新一輪傳遞結束標記(overSet)
					self.ColliedWith(orishift,other,over)#here we go!!!
					
					#反击退自己--------------------------------------
					over=[other]#放other是为了省一个angleBetween,因为短路效应当第一条件not in overSet失败之后就直接跳出了
					self.ColliedWith(-orishift,circle,over)#反击退方向相反所以加一个负号
			#print("aft cal circle{0} position is{1}".format(circle.id,circle.center))
		#print("end collied-------------------------------------")
		for node in self.record:
			for circle in node.subNode:
				oriPos=circle.center
				realshift=self.closeSet[circle.id].shift
				#print("no{1} realshift{0}".format(realshift,circle.id))
				#计算是否超过边界
				if circle.center.x+realshift.x>self.circles.leftBoundary and circle.center.x+realshift.x<self.circles.rightBoundary:#在边界内
					#print("in add shift center{0} realshift{1}".format(circle.center,realshift.x))
					if not realshift.x == 0:
						circle.center.x+=realshift.x
					#print("after add center.x:{0}".format(circle.center.x))
					#circle.lastShiftx+=realshift.x
					#print("id{0} lastShift x-1:{1}".format(circle.id,circle.lastShiftx))
				elif circle.center.x+realshift.x<=self.circles.leftBoundary:#超出左边界
					realshift.x=self.circles.leftBoundary- circle.center.x
					circle.center.x=self.circles.leftBoundary
					#circle.center.x+=self.circles.leftBoundary
					#circle.lastShiftx+=self.circles.leftBoundary-circle.center.x
					print("lastShift x-2")
				else:#超出右边界
					realshift.x=self.circles.rightBoundary- circle.center.x
					circle.center.x=self.circles.rightBoundary
					#circle.lastShiftx+=self.circles.rightBoundary-circle.center.x
					print("lastShift x-3")
				if circle.center.y+realshift.y>self.circles.upBoundary and circle.center.y+realshift.y<self.circles.downBoundary: #在边界内
					if not realshift.y == 0:
						circle.center.y+=realshift.y
					#circle.lastShifty+=realshift.y
					#print("id{0} lastShift y-1:{1}".format(circle.id,circle.lastShifty))
				elif circle.center.y+realshift.y<=self.circles.upBoundary:#超出上边界
					realshift.y=self.circles.upBoundary- circle.center.y
					circle.center.y=self.circles.upBoundary
					#circle.lastShifty=self.circles.upBoundary-realshift.y
					print("lastShift y-2")
				else:#超出下边界
					realshift.y=self.circles.downBoundary- circle.center.y
					circle.center.y=self.circles.downBoundary
					#circle.lastShifty+=self.circles.downBoundary-realshift.y
					print("lastShift y-3")
				print("no{0} set shift ok".format(circle.id))
				self.shiftCallBack(circle.id,realshift.x,realshift.y)
				#改变XYTree
				self.closeSet[circle.id].shift=Vector2(0,0)
				#print("shift为:"+str(self.closeSet[circle.id].shift))

				#print("in the circle end circle.center{0} id{1}".format(circle.center,id(circle.center)))
				#print("in end of collied shift({0},{1})".format(circle.lastShiftx,circle.lastShifty))
		#for node in self.record:
		#	for circle in node.subNode:
		#		print("in the end circle.center{0} id{1}".format(circle.center,id(circle.center)))
	
	def CastWithCloser(self,centerX,centerY,radiu,sameOwner=0,ownerId=-1):#用于角色攻击目标判断,会省略和cast点相同坐标的圆,所以不能用来技能范围判断
#ownerId为-1时为sameOwner为1,或-1都没有用,ownerId为阵营判断基准,sameOwner为1时判定相同
#暂时使用线性搜寻,可能不是暂时...
		closer=None
		answer=[]
		#print("in cast same:{0} id:{1} record.len{2}".format(sameOwner,ownerId,len(self.record)))
		if sameOwner==0:#无视阵营遍历
		#	print("sameOwner==0")
			for node in self.record:
				for circle in node.subNode:
					arrow=Vector2(circle.center.x-centerX,circle.center.y-centerY)
		#			print("arrow mag{0} radiu+circle.radiu{1}".format(arrow.magnitude,radiu+circle.radiu))
					if (closer==None or closer.center.magnitude>arrow.magnitude)and not arrow.magnitude==0:
		#				print("closer = {0}".format(arrow.magnitude))
						closer=circle
					if arrow.magnitude<radiu+circle.radiu and not arrow.magnitude==0:
		#				print("answer append {0}".format(arrow.magnitude))
						answer.append(circle)
		else:
			if ownerId==-1:
				return {'closer':closer,'answer':answer}
			elif sameOwner==1:#回传相同阵营
				for node in self.record:
					for circle in node.subNode:
						arrow=Vector2(circle.center.x-centerX,circle.center.y-centerY)
						if (closer==None or closer.center.magnitude>arrow.magnitude)and (circle.ownerid==ownerId and not arrow.magnitude==0):
							closer=circle
						if arrow.magnitude<radiu+circle.radiu and circle.ownerid==ownerId and not arrow.magnitude==0:
							answer.append(circle)
			elif sameOwner==-1:#回传不同阵营
				for node in self.record:
					for circle in node.subNode:
						arrow=Vector2(circle.center.x-centerX,circle.center.y-centerY)
						if (closer==None or closer.center.magnitude>arrow.magnitude)and (not circle.ownerid==ownerId and  not arrow.magnitude==0):
							closer=circle
						if arrow.magnitude<radiu+circle.radiu and not circle.ownerid==ownerId and not arrow.magnitude==0:
							answer.append(circle)
		return {'closer':closer,'answer':answer}
	def getSortedCircleList(self,maincenter):#根据距离从近到远
		sortList=[]
		#print("in bulid sort list")
		for node in self.record:
				for circle in node.subNode:
					distant= (circle.center- maincenter).magnitude
		#			print("no{0} dist{1}")
					if len(sortList)==0:
						#print("enter 1")
						sortList.append(Pair(circle,distant))
					else:
						#print("enter 0")
						if sortList[0].value>=distant:
							#print("enter 01")
							sortList.insert(0,Pair(circle,distant))
						else:
							#print("enter 00")
							for i in range(0,len(sortList)):
								if i+1>=len(sortList):#扫到尾部
									#print("enter 001")
									if sortList[i].value<distant:
										#print("")
										sortList.append(Pair(circle,distant))
									else:
										sortList.insert(i,Pair(circle,distant))
									break
								elif sortList[i].value<distant and sortList[i+1].value>=distant:
									#print("enter 000")
									sortList.insert(i+1,Pair(circle,distant))
									break
		'''			templist=[]
					for pair in sortList:
						templist.append([pair.key.id,pair.value])
					print(templist)'''
		return sortList
#class XYCollied end ----------------------------------------------------------------------------------------------------------------------
'''
import pygame
from pygame.locals import *
from pygame.color import *
# pygame初始設定
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
crashed=False
clock.tick(30)
#文字部分
pygame.font.init()
font = pygame.font.Font(None, 20)
#相鄰集合:每一次碰撞計算(LinerCollied)重置一次,因為上一次位移註定會改變相鄰的狀態
closeSet={}
#圓集合:不重置
circles=[]
#circles=[Circle(Vector2(474.40635724908134,175.2827185671207),20,94),Circle(Vector2(464.9034937978259,136.4279173926942),20,87)]
#circles=[Circle(Vector2(100,100-20/math.sqrt(3)),20,0),Circle(Vector2(90,100+(10/math.sqrt(3))),20,1),(Circle(Vector2(110,100+(10/math.sqrt(3))),20,2))]
#circles=[Circle(Vector2(90,100+(10/math.sqrt(3))),20,1),(Circle(Vector2(110,100+(10/math.sqrt(3))),20,2)),Circle(Vector2(100,100-20/math.sqrt(3)),20,0)]
#已分配id的數量
idNum=0
def ColliedWith(shift,circle,overSet):#用於遞迴分散位移
	if(not circle.id in closeSet):#還未記錄與相鄰列表
		closeSet[circle.id]=CloseSetNode(circle)#新增屬於此圓相鄰集合的節點
		for other in circles:#線性搜尋向交或相鄰的其他圓
			if not other == circle:
				distant=Vector2.distantBetween(circle.center,other.center)
				if distant <=(circle.radiu+other.radiu):#距離小於等於半徑之和說明相交或相鄰
					closeSet[circle.id].closer.append(other)
	#給自己一個位移
	closeSet[circle.id].shift+=shift
	overSet.append(circle)#將自己標記成傳遞over
	#開始分散位移
	for other in closeSet[circle.id].closer:
		#print("shift:{0}other.center-circle.center:{1}".format(shift,other.center-circle.center))
		if not other in overSet and Vector2.angleBetween(shift,other.center-circle.center)<=(math.pi*0.5):#如果目標圓還沒有傳遞過,並且相對圓心和位移的夾角小於90度
			#print("{0}->{1}-------------------------------".format(circle.id,other.id))
			ColliedWith(shift,other,overSet)#去吧少年
def LinerCollied():
	for circle in circles:#因為用線性搜尋所以才叫LinerCollied,呵呵.每個圓形只計算自己對其他圓形的擊退距離,和一個自己被反擊退的距離
		if(not circle.id in closeSet):#還未記錄自己的與相鄰列表
			closeSet[circle.id]=CloseSetNode(circle)#新增屬於此圓相鄰集合的節點
			for other in circles:#線性搜尋向交或相鄰的其他圓
				if not other == circle:
					distant=Vector2.distantBetween(circle.center,other.center)
					if distant <=(circle.radiu+other.radiu):#距離小於等於半徑之和說明相交或相鄰
						closeSet[circle.id].closer.append(other)
		for other in closeSet[circle.id].closer:
			#print("Liner {0}{1}->{2}{3}-------------------------------".format(circle.id,circle.center,other.id,other.center))
			#nowCenter對方當前推算過位移(shift)的圓心
			if other.id in closeSet:#這個判斷是為了防止對方還沒有記錄與closeSet中,沒記錄說明shift為無
				nowCenter=other.center+closeSet[other.id].shift#這個nowCenter是根據當前位移和原圓心位置推導出來的當前圓心位置
			else:
				nowCenter=other.center
			
			#nowCircleCenter自己當前推算過位移(shift)的圓心
			nowCircleCenter=circle.center+closeSet[circle.id].shift
			
			halfOverlap=(circle.radiu+other.radiu-Vector2.distantBetween(nowCircleCenter,nowCenter))/2#半徑之和減去圓心距離可知道兩個圓重疊半徑
			if round(halfOverlap,1) <=0:#如果舍去至一位小數後為0則不做,說明擠壓度太小了可以忽略,这样可以防止重复击退:A击退B,那么理论上A和B的距离应该为0,所以当B计算时会在这里略过A
				continue
			#print("halfOverlap is {0}".format(halfOverlap))
			orishift=((nowCenter-circle.center).normalized).scaleWith(halfOverlap)#放大指向目標圓心的單位向量,這將是本次的shift
			#print("origen shift is:{0}".format(orishift))
			#击退--------------------------------------------
			over=[circle]#新一輪傳遞結束標記(overSet)
			ColliedWith(orishift,other,over)#here we go!!!
			
			#反击退自己--------------------------------------
			over=[other]#放other是为了省一个angleBetween,因为短路效应当第一条件not in overSet失败之后就直接跳出了
			ColliedWith(-orishift,circle,over)#反击退方向相反所以加一个负号
			
	#print("end collied-------------------------------------")
	#for circle in circles:
	#	print("{0}:{1}".format(circle.id,circle.center))
#正式代碼
#print(Vector2.angleBetween(Vector2(0,1),Vector2(math.sqrt(3)/2,-0.5))/math.pi)
#print(Vector2.angleBetween(Vector2(0,1),Vector2(-1,0))/math.pi)
#task={1:"Jhon"}
#print(1 in task)
#print(Vector2(99,99).normalized)
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
while not crashed:
	screen.fill(THECOLORS["white"])
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		elif event.type == MOUSEBUTTONDOWN and event.button == 1:
			Pos=Vector2(event.pos[0],event.pos[1])
			print("添加圓{1} 圓心:{0}".format(Pos,idNum))
			circles.append(Circle(Pos,20,idNum))
			idNum+=1
		elif event.type == MOUSEBUTTONDOWN and event.button == 3:#一鍵結算碰撞
			start=time.time()
			print("start:{0}".format(start))
			closeSet={}#重置相鄰集合
			LinerCollied()#走起
			for key in closeSet:#移動碰撞後最終位移值
				closeSet[key].owner.center+=closeSet[key].shift
			print("end:{0}".format(time.time()))
			#print("end collied-------------------------------------")
			#for circle in circles:
			#	print("{0}:{1}".format(circle.id,circle.center))
	for obj in circles:
		pygame.draw.circle(screen, THECOLORS["blue"],[int(obj.center.x),int(obj.center.y)],obj.radiu, 2)
		msg_surf = font.render(str(obj.id), 1, pygame.Color('black'))
		screen.blit(msg_surf,(int(obj.center.x),int(obj.center.y)))
	pygame.display.flip()
'''
'''
import pygame
from pygame.locals import *
from pygame.color import *
# pygame初始設定
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
crashed=False
clock.tick(30)
#文字部分
pygame.font.init()
font = pygame.font.Font(None, 20)

space=XYCollied(10,10,0,0,60,60)
#space.addCircle(Vector2(414,200),20)
#space.addCircle(Vector2(418,193),20)
#space.addCircle(Vector2(414,200)+Vector2(-8,14),20)
#space.addCircle(Vector2(418,193)+Vector2(8,-14),20)
space.addCircle(Vector2(306,148),20)
space.addCircle(Vector2(328,156),20)
space.addCircle(Vector2(315,166),20)
while not crashed:
	screen.fill(THECOLORS["white"])
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		elif event.type == MOUSEBUTTONDOWN and event.button == 1:
			Pos=Vector2(event.pos[0],event.pos[1])
			new=space.addCircle(Pos,20)
			print("++++++++++++++++++++++++++++add circle"+str(new))
		elif event.type == MOUSEBUTTONDOWN and event.button == 3:#一鍵結算碰撞
			start=time.time()
			space.Collied()
			#for area in space.record:
			#	for circle in area.subNode:
			#		print("{0}:{1}".format(circle.id,circle.center))
			print("经历时间:{0}".format(time.time()-start))
	for area in space.record:
		for obj in area.subNode:
			pygame.draw.circle(screen, THECOLORS["blue"],[int(obj.center.x),int(obj.center.y)],obj.radiu, 2)
			msg_surf = font.render(str(obj.id), 1, pygame.Color('black'))
			screen.blit(msg_surf,(int(obj.center.x),int(obj.center.y)))
	pygame.display.flip()
'''