from ColliedSpace import Vector2

ONLY_UNIT=0
MUTI_UNITS=1
UNIT_POS=2
ONLY_POS=3
MUTI_POS=4
class ActionCard:
	def __init__(self,manager):
		self.manager=manager
	def action(self,dict):
		pass
		

class PuppetSurgery(ActionCard):
	def action(self,dict):
		self.manager.transmission(dict["unitNo"],Vector2(dict["position"][0],dict["position"][1]))
cardClassList=[PuppetSurgery]
def getList(manager):
	ans=[]
	for c in cardClassList:
		ans.append(c(manager))
	return ans