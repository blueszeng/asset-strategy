import KBEngine
from KBEDebug import *

class WarField(KBEngine.Base):
	def __init__(self):
		KBEngine.Base.__init__(self)
		DEBUG_MSG("WarField Base done")
		self.createInNewSpace(None)