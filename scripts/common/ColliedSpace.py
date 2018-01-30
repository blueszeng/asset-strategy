import math

import sys

import XYTree
import time

class Circle:
	def __init__(self,center,radiu,id):#id用來快速檢索closeset
		self.center=center
		self.radiu=radiu 
		self.id=id
		self.lastShiftx=0
		self.lastShifty=0
	def __str__(self):
		return "id:"+str(self.id)+":"+str(self.center)+"radiu:"+str(self.radiu)

class Vector2:
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.magnitude=math.sqrt(x*x+y*y)#向量長度
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
		return math.acos((first*second)/(first.magnitude*second.magnitude))
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
	def addCircle(self,position,radiu):
		if	len(self.circles.getNode(position.x,position.y).subNode)==0:#如果node里没有装载节点
			self.record.append(self.circles.getNode(position.x,position.y))
		circle=Circle(position,radiu,self.totalNum)
		self.circles.addUnit(position.x,position.y,Circle(position,radiu,self.totalNum))
		self.totalNum+=1
		return circle
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
		#print("end collied-------------------------------------")
		for node in self.record:
			for circle in node.subNode:
				oriPos=circle.center
				realshift=self.closeSet[circle.id].shift
				#计算是否超过边界
				if circle.center.x+realshift.x>self.circles.leftBoundary and circle.center.x+realshift.x<self.circles.rightBoundary:#在边界内
					circle.center.x+=realshift.x
					#circle.lastShiftx+=realshift.x
					#print("id{0} lastShift x-1:{1}".format(circle.id,circle.lastShiftx))
				elif circle.center.x+realshift.x<=self.circles.leftBoundary:#超出左边界
					circle.center.x+=self.circles.leftBoundary
					#circle.lastShiftx+=self.circles.leftBoundary-circle.center.x
					#print("lastShift x-2")
				else:#超出右边界
					circle.center.x=self.circles.rightBoundary
					#circle.lastShiftx+=self.circles.rightBoundary-circle.center.x
					#print("lastShift x-3")
				if circle.center.y+realshift.y>self.circles.upBoundary and circle.center.y+realshift.y<self.circles.downBoundary: #在边界内
					circle.center.y+=realshift.y
					#circle.lastShifty+=realshift.y
					#print("id{0} lastShift y-1:{1}".format(circle.id,circle.lastShifty))
				elif circle.center.y+realshift.y<=self.circles.upBoundary:#超出上边界
					circle.center.y+=self.circles.upBoundary
					#circle.lastShifty=self.circles.upBoundary-realshift.y
					#print("lastShift y-2")
				else:#超出下边界
					circle.center.y=self.circles.downBoundary
					#circle.lastShifty+=self.circles.downBoundary-realshift.y
					#print("lastShift y-3")
				self.shiftCallBack(circle.id,realshift.x,realshift.y)
				#改变XYTree
				self.closeSet[circle.id].shift=Vector2(0,0)
				#print("shift为:"+str(self.closeSet[circle.id].shift))
				if not self.circles.inSameArea(oriPos.x,oriPos.y,circle.center.x,circle.center.y):#如果移动之后会进入一个新的区域
					node.subNode.remove(circle)
					if len(node.subNode)==0:
						self.record.remove(node)
					newnode=self.circles.getNode(circle.center.x,circle.center.y)
					newnode.subNode.append(circle)
					if not newnode in self.record:
						self.record.append(newnode)
				#print("in end of collied shift({0},{1})".format(circle.lastShiftx,circle.lastShifty))

	
	def CastWithCloser(self,centerX,centerY,radiu,sameOwner=0,selfid=-1):
#selfid为-1时为sameOwner为1,或-1都没有用,selfid为阵营判断基准,sameOwner为1时判定相同
#暂时使用线性搜寻,可能不是暂时...
		closer=None
		answer=[]
		print("in cast same:{0} id:{1} record.len{2}".format(sameOwner,selfid,len(self.record)))
		if sameOwner==0:#无视阵营遍历
			print("sameOwner==0")
			for node in self.record:
				for circle in node.subNode:
					arrow=Vector2(circle.center.x-centerX,circle.center.y-centerY)
					print("arrow mag{0} radiu+circle.radiu{1}".format(arrow.magnitude,radiu+circle.radiu))
					if (closer==None or closer.magnitude>arrow.magnitude)and not selfid==circle.id:
						closer=circle
					if arrow.magnitude<radiu+circle.radiu:
						answer.append(circle)
		else:
			if selfid==-1:
				return {'closer':closer,'answer':answer}
			elif sameOwner==1:#回传相同阵营
				for node in self.record:
					for circle in node.subNode:
						arrow=Vector2(circle.center.x-centerX,circle.center.y-centerY)
						if (closer==None or closer.magnitude>arrow.magnitude)and circle.ownerid==selfid:
							closer=circle
						if arrow.magnitude<radiu+circle.radiu and circle.ownerid==selfid:
							answer.append(circle)
			elif sameOwner==-1:#回传不同阵营
				for node in self.record:
					for circle in node.subNode:
						arrow=Vector2(circle.center.x-centerX,circle.center.y-centerY)
						if (closer==None or closer.magnitude>arrow.magnitude)and not circle.ownerid==selfid:
							closer=circle
						if arrow.magnitude<radiu+circle.radiu and not circle.ownerid==selfid:
							answer.append(circle)
		return {'closer':closer,'answer':answer}
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