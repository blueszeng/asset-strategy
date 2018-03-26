from AI import AI
from damage import Damage
list={}
#no0 狐族双剑士
list[0]=[0,1,2,3]
#no1 流浪炎术士
list[1]=[4,5,6,7]
#no2 陣線先鋒
list[2]=[8]
#no3 皇家神射手
list[3]=[9,10,11]

ranges={}
ranges[0]=AI.NEAR_RANGE(2)
ranges[1]=AI.FAR_RANGE(2)
ranges[2]=AI.NEAR_RANGE(2)
ranges[3]=AI.FAR_RANGE(2)

propertys={}
propertys[0]=[30,Damage.LIGHT_ARMOR(),100]
propertys[1]=[10,Damage.CLOTH_ARMOR(),80]
propertys[2]=[50,Damage.HEAVY_ARMOR(),120]
propertys[3]=[10,Damage.CLOTH_ARMOR(),80]