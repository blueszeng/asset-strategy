"""
				XYTree
		       /   |  \
			  Y    Y   Y
		     /|\
		    X X X
		   /|
		 u1 u2
		 
		node0 <-left- node1 <-left- node3 <-left- node4
		node0 -right-> node1 -right-> node3 -right-> node4
"""
import math

class XYTreeNode:
	def __init__(self):
		self.subNode=[]
class YTreeNode(XYTreeNode):
	def __init__(self,left):
		super().__init__()
		self.left=left
		self.right=None
		if not left == None:
			left.right=self
class XTreeNode(YTreeNode):
	def __init__(self,left,up,No):
		super().__init__(left)
		self.up=up
		self.down=None
		if not up == None:
			up.down=self
		self.No=No
	def getIndexX(self,tree):
		return self.No%tree.xnum
	def getIndexY(self,tree):
		return int(self.No/tree.xnum)
class XYTree:
	def __init__(self,x,y,leftBoundary,upBoundary,cellWidth,cellHeight):
		self.ynum=y
		self.xnum=x
		self.yNodes=[]#坐标节点的集合
		for i in range(0,y):
			print('y='+str(i)+'-----------------------------------')
			if i==0:
				nowy=YTreeNode(None)
			else:
				nowy=YTreeNode(self.yNodes[len(self.yNodes)-1])
			for j in range(0,x):#编织X节点的网状结构
				upperX=None
				if i>0:
					upperX=self.yNodes[i-1].subNode[j]
				if j==0:#如果是第一个节点,左边当然不会有节点
					nowx=XTreeNode(None,upperX,i*x+j)
				else:
					nowx=XTreeNode(nowy.subNode[len(nowy.subNode)-1],upperX,i*x+j)
				print("x="+str(j))
				nowy.subNode.append(nowx)
			self.yNodes.append(nowy)
#这四项属性用来从坐标推算索引值
		self.leftBoundary=leftBoundary#最坐标的边界x值
		self.upBoundary=upBoundary#最上方的边界y值
		self.cellWidth=cellWidth#每个节点方块的宽度(x)
		self.cellHeight=cellHeight#每个节点方块的长度(y)
	@property
	def downBoundary(self):
		return self.upBoundary+self.ynum*self.cellHeight
	@property
	def rightBoundary(self):
		return self.leftBoundary+self.xnum*self.cellWidth
	def getNode(self,posx,posy):
		indexX=math.floor((round(posx,3)-round(self.leftBoundary,3))/round(self.cellWidth,3))
		indexY=math.floor((round(posy,3)-round(self.upBoundary,3))/round(self.cellHeight,3))
		#如果超过边界则放在那个边界,但如果大量的物件都放在边界的话,会变为线性搜寻,效率低下
		if indexY<0:#超过y上边边界
			indexY=0
		elif indexY>=len(self.yNodes):#超过y下边边界
			indexY=len(self.yNodes)-1
		if indexX<0:#超过x左边边界
			indexX=0
		elif indexX>=len(self.yNodes[indexY].subNode):#超过x右边边界
			indexX=len(self.yNodes[indexY].subNode)-1
		return self.yNodes[indexY].subNode[indexX]
	def addUnit(self,posx,posy,unit):
		self.getNode(posx,posy).subNode.append(unit)#放入
	def __str__(self):
		string="XYTree(left:{0},up:{1},width:{2},height:{3}):".format(self.leftBoundary,self.upBoundary,self.cellWidth,self.cellHeight)
		for y in range(0,len(self.yNodes)):
			string+="\n y({0}-{1})len:{2}:".format(self.upBoundary+y*self.cellHeight,self.upBoundary+(y+1)*self.cellHeight,len((self.yNodes[y]).subNode))
			for x in range(0,len(self.yNodes[y].subNode)):
				nownode=self.yNodes[y].subNode[x]
				temp=''#这个用来检测x网络是否连接正确
				'''if(nownode.left!=None):
					temp+="left:{0}".format(nownode.left.No)
				if(nownode.up!=None):
					temp+="up:{0}".format(nownode.up.No)
				if(nownode.right!=None):
					temp+="right:{0}".format(nownode.right.No)
				if(nownode.down!=None):
					temp+="down:{0}".format(nownode.down.No)'''
				string+=("\n ->x=({0}-{1})"+temp+":").format(self.leftBoundary+x*self.cellWidth, self.leftBoundary+(x+1)*self.cellWidth)
				
				for node in self.yNodes[y].subNode[x].subNode:
					string+=("\n ->->"+str(node))
		return string
	def inSameArea(self,firstx,firsty,secondx,secondy):
		boolx=(math.floor(round(firstx,3)/round(self.cellWidth,3))==math.floor(round(secondx,3)/round(self.cellWidth,3)))
		booly=(math.floor(round(firsty,3)/round(self.cellHeight,3))==math.floor(round(secondy,3)/round(self.cellHeight)))
		return boolx and booly
#----------------------------------------------测试代码---------------------------------------------
'''tree=XYTree(6,6,-15.5,-100,30,30)
tree.addUnit(-10,-10,1)
tree.addUnit(100.77,60,2)
tree.addUnit(500,500,3)
print(tree)'''

