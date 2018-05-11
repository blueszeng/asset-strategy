
class gird:
	def __init__(self,posx,posy,width,length):
		self.width=float(width)
		self.length=float(length)
		self.centerPos=[]
		self.centerPos.append(float(posx)+width/2)
		self.centerPos.append(float(posy)+length/2)
		self.inside=None#我感到空虚
	def __str__(self):
		return str(self.centerPos)+" wid:"+str(self.width)+" len:"+str(self.length)+"inside:"+str(self.inside)
class gridMaskCreater:
	def __init__(self,orix,oriy,unitwid,unitlen,xnum,ynum):
		self.grids=[]
		self.unitwid=unitwid
		self.unitlen=unitlen
		for y in range(0,ynum):
			xline=[]
			for x in range(0,xnum):
				xline.append(gird(orix+x*unitwid,oriy+y*unitlen,unitwid,unitlen))
			self.grids.append(xline)
	def castGird(posx,posy):
		y=int((posy-grids.oriy)/unitlen)
		x=int((posx-grids.orix)/unitwid)
		return self.grids[y][x]
	def printGirds(self):
		for list in self.grids:
			print("-------------------------------------")
			for gird in list:
				print(gird)
	def getIdleGridList(self):#回传一个包含 所有inside为None的grid 的List
		vaildGrids=[]
		for xlist in self.grids:
			for grid in xlist:
				if grid.inside==None:
					vaildGrids.append(grid)
		return vaildGrids
#储存预设地形的工具
class itemIndex:#记录预设的陷阱索引
	def __init__(self,indexX,indexY,big=True):#big标记是否是占用4格的陷阱
		self.indexX=indexX#如果是4格陷阱indexX/Y请给 以ColliedSpace坐标系来看 左上的那个格子
		self.indexY=indexY
		self.big=big
		print("itemIndex init: "+str(indexX)+","+str(indexY))
	def getCenter(self,girdMask):#输入值应该是一个list,是二维阵列 为gridMaskCreater.grids而制作
		gird=girdMask[self.indexY][self.indexX]
		if self.big:
			return [gird.centerPos[0]+gird.width/2,gird.centerPos[1]+gird.length/2]
		else:
			return gird.centerPos[:]
	def enteMask(self,girdMask,obj):
		if self.big:#大的物件将占据4格
			girdMask[self.indexY][self.indexX].inside=obj
			girdMask[self.indexY+1][self.indexX].inside=obj
			girdMask[self.indexY][self.indexX+1].inside=obj
			girdMask[self.indexY+1][self.indexX+1].inside=obj
		else:
			girdMask[self.indexY][self.indexX].inside=obj

Map1=[itemIndex(6,0),itemIndex(0,4),itemIndex(2,4),itemIndex(6,6),itemIndex(0,8),itemIndex(4,10),itemIndex(6,10),itemIndex(0,14)]