from gridMaskCreater import gridMaskCreater
from gridMaskCreater import Map1

creater= gridMaskCreater(-8,-16,2,2,8,16)
creater.printGirds()

id = 1
for item in Map1:
	item.enteMask(creater.grids,id)
	id+=1
	
creater.printGirds()